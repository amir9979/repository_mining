import difflib
from subprocess import Popen, PIPE
import tempfile
import os
import shutil


class MethodData(object):
    def __init__(self, method_name, start_line, end_line):
        self.method_name = method_name
        self.start_line = int(start_line)
        self.end_line = int(end_line)

    def is_changed(self, indices):
        return any(filter(lambda ind: ind >= self.start_line and ind <= self.end_line, indices))

    def __repr__(self):
        return self.method_name


class FileDiff(object):
    REMOVED = '- '
    ADDED = '+ '
    UNCHANGED = '  '
    NOT_IN_INPUT = '? '
    BEFORE_PREFIXES = [REMOVED, UNCHANGED]
    AFTER_PREFIXES = [ADDED, UNCHANGED]
    EXTERNALS_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../externals"))
    CHECKSTYLE_PATH = os.path.join(EXTERNALS_PATH, "checkstyle-6.8-SNAPSHOT-all.jar")
    CHECKSTYLE_XML_PATH = os.path.join(EXTERNALS_PATH, "methodNameLines.xml")

    def __init__(self, diff):
        self.file_name = diff.b_path
        if not self.file_name.endswith(".java"):
            return
        self.before_contents = ['']
        if diff.new_file:
            assert diff.a_blob is None
        else:
            self.before_contents = diff.a_blob.data_stream.stream.readlines()
        self.after_contents = ['']
        if diff.deleted_file:
            assert diff.b_blob is None
        else:
            self.after_contents = diff.b_blob.data_stream.stream.readlines()
        assert self.before_contents != self.after_contents
        self.before_indices, self.after_indices = self.get_changed_indices()
        self.changed_methods = FileDiff.get_methods_lines(self.before_contents, self.before_indices) + \
                               FileDiff.get_methods_lines(self.after_contents, self.after_indices)

    def is_source_file(self):
        return self.file_name.endswith(".java")

    def get_changed_indices(self):
        def get_lines_by_prefixes(lines, prefixes):
            return filter(lambda x: any(map(lambda p: x.startswith(p), prefixes)), lines)

        def get_indices_by_prefix(lines, prefix):
            return map(lambda x: x[0], filter(lambda x: x[1].startswith(prefix), enumerate(lines)))

        diff = list(difflib.ndiff(self.before_contents, self.after_contents))

        diff_before_lines = get_lines_by_prefixes(diff, self.BEFORE_PREFIXES)
        assert map(lambda x: x[2:], diff_before_lines) == self.before_contents
        before_indices = get_indices_by_prefix(diff_before_lines, self.REMOVED)

        diff_after_lines = get_lines_by_prefixes(diff, self.AFTER_PREFIXES)
        assert map(lambda x: x[2:], diff_after_lines) == self.after_contents
        after_indices = get_indices_by_prefix(diff_before_lines, self.ADDED)

        return before_indices, after_indices

    @staticmethod
    def get_methods_lines(contents, indices):
        out_dir = tempfile.mkdtemp()
        before_path = os.path.join(out_dir, "contents.java")
        with open(before_path, "wb") as f:
            f.writelines(contents)
        checkstyle_out_path = os.path.join(out_dir, "checkstyle")
        run_commands = ["java", "-jar", FileDiff.CHECKSTYLE_PATH, "-c", FileDiff.CHECKSTYLE_XML_PATH, "javaFile", "-o",
                        checkstyle_out_path, out_dir]
        proc = Popen(run_commands, stdout=PIPE, stderr=PIPE, shell=True)
        (out, err) = proc.communicate()
        with open(checkstyle_out_path) as f:
            lines = f.readlines()[1:-1]
            methods = map(lambda line: MethodData(*line.split()[1].split("@")), lines)
        shutil.rmtree(out_dir)
        return filter(lambda method: method.is_changed(indices), methods)

