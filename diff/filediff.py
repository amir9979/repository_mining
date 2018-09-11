import difflib
from subprocess import Popen, PIPE
import tempfile
import gc


class FileDiff(object):
    REMOVED = '- '
    ADDED = '+ '
    UNCHANGED = '  '
    NOT_IN_INPUT = '? '
    BEFORE_PREFIXES = [REMOVED, UNCHANGED]
    AFTER_PREFIXES = [ADDED, UNCHANGED]

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

    def get_changed_methods(self):
        pass


def get_methods_lines(contents):
    with tempfile.TemporaryFile() as f:
        f.writelines(contents)
        run_commands = ["java", "-jar", checkStyle68, "-c", methodNameLines, "javaFile", "-o", outPath, workingDir]
        proc = Popen(run_commands, stdout=PIPE, stderr=PIPE, shell=True)
        (out, err) = proc.communicate()


