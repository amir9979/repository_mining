import difflib
from subprocess import Popen, PIPE
import tempfile
import os
import shutil
import javalang
import operator


class MethodData(object):
    def __init__(self, method_name, start_line, end_line, contents, indices, parameters=None):
        self.method_name = method_name
        self.start_line = int(start_line)
        self.end_line = int(end_line)
        self.implementation = contents[self.start_line-1: self.end_line]
        self.changed = self._is_changed(indices)
        self.parameters = parameters
        self.id = self.method_name + "(" + ",".join(self.parameters) + ")"

    def _is_changed(self, indices):
        return any(filter(lambda ind: ind >= self.start_line and ind <= self.end_line, indices))

    def __eq__(self, other):
        assert isinstance(other, type(self))
        return self.method_name == other.method_name and self.parameters == other.parameters

    def __repr__(self):
        return self.id


class SourceFile(object):
    def __init__(self, contents, indices, file_name):
        self.contents = contents
        self.changed_indices = indices
        self.file_name = file_name
        if file_name.endswith(".java"):
            self.tokens = list(javalang.tokenizer.tokenize("".join(self.contents)))
            self.parser = javalang.parser.Parser(self.tokens)
            self.parsed_data = self.parser.parse()
            packages = map(operator.itemgetter(1), self.parsed_data.filter(javalang.tree.PackageDeclaration))
            self.package_name = ''
            if packages:
                self.package_name = packages[0].name
            self.methods = self.get_methods_by_javalang()

    def _get_methods(self):
        out_dir = tempfile.mkdtemp()
        before_path = os.path.join(out_dir, "contents.java")
        with open(before_path, "wb") as f:
            f.writelines(self.contents)
        checkstyle_out_path = os.path.join(out_dir, "checkstyle")
        run_commands = ["java", "-jar", FileDiff.CHECKSTYLE_PATH, "-c", FileDiff.CHECKSTYLE_XML_PATH, "javaFile", "-o",
                        checkstyle_out_path, out_dir]
        proc = Popen(run_commands, stdout=PIPE, stderr=PIPE, shell=True)
        proc.communicate()
        with open(checkstyle_out_path) as f:
            lines = map(lambda line: line.split()[1].split("@"), f.readlines()[1:-1])
            methods = dict()
            for method_name, start_line, end_line in lines:
                methods[method_name] = MethodData(method_name, start_line, end_line, self.contents, self.changed_indices)
        shutil.rmtree(out_dir)
        return methods

    def get_methods_by_javalang(self):
        def get_method_end_position(method, seperators):
            method_seperators = seperators[map(id, sorted(seperators + [method], key=lambda x: (x.position.line, x.position.column))).index(id(method)):]
            assert method_seperators[0].value == "{"
            counter = 1
            for seperator in method_seperators[1:]:
                if seperator.value == "{":
                    counter += 1
                elif seperator.value == "}":
                    counter -= 1
                if counter == 0:
                    return seperator.position

        seperators = filter(lambda token: isinstance(token, javalang.tokenizer.Separator) and token.value in "{}", self.tokens)
        methods_dict = dict()
        for class_declaration in map(operator.itemgetter(1), self.parsed_data.filter(javalang.tree.ClassDeclaration)):
            class_name = class_declaration.name
            methods = map(operator.itemgetter(1), self.parsed_data.filter(javalang.tree.MethodDeclaration))
            constructors = map(operator.itemgetter(1), self.parsed_data.filter(javalang.tree.ConstructorDeclaration))
            for method in methods + constructors:
                if not method.body:
                    # skip abstract methods
                    continue
                method_start_position = method.position
                method_end_position = get_method_end_position(method, seperators)
                parameters = map(lambda parameter: parameter.type.name, method.parameters)
                method_data = MethodData(".".join([self.package_name,class_name,method.name]), method_start_position.line, method_end_position.line,
                                         self.contents, self.changed_indices, parameters)
                methods_dict[method_data.id] = method_data
        return methods_dict



    def get_changed_methods(self):
        return filter(lambda method: method.is_changed, self.methods.values())

    def replace_method(self, method_data):
        assert method_data.method_name in self.methods
        old_method = self.methods[method_data.method_name]
        self.contents = self.contents[:old_method.start_line] + \
                        self.contents[method_data.start_line:method_data.end_line] + \
                        self.contents[old_method.end_line:]
        self.methods = self.get_methods_by_javalang()


    def __repr__(self):
        return self.file_name


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

    def __init__(self, diff, commit_sha):
        self.file_name = diff.b_path
        self.commit_sha = commit_sha
        if not self.is_java_file():
            return
        before_contents = ['']
        if diff.new_file:
            assert diff.a_blob is None
        else:
            before_contents = diff.a_blob.data_stream.stream.readlines()
        after_contents = ['']
        if diff.deleted_file:
            assert diff.b_blob is None
        else:
            after_contents = diff.b_blob.data_stream.stream.readlines()
        before_indices, after_indices = self.get_changed_indices(before_contents, after_contents)
        self.before_file = SourceFile(before_contents, before_indices, diff.a_path)
        self.after_file = SourceFile(after_contents, after_indices, diff.b_path)

    def is_java_file(self):
        return self.file_name.endswith(".java")

    @staticmethod
    def get_changed_indices(before_contents, after_contents):
        def get_lines_by_prefixes(lines, prefixes):
            return filter(lambda x: any(map(lambda p: x.startswith(p), prefixes)), lines)

        def get_indices_by_prefix(lines, prefix):
            return map(lambda x: x[0], filter(lambda x: x[1].startswith(prefix), enumerate(lines)))

        diff = list(difflib.ndiff(before_contents, after_contents))

        diff_before_lines = get_lines_by_prefixes(diff, FileDiff.BEFORE_PREFIXES)
        assert map(lambda x: x[2:], diff_before_lines) == before_contents
        before_indices = get_indices_by_prefix(diff_before_lines, FileDiff.REMOVED)

        diff_after_lines = get_lines_by_prefixes(diff, FileDiff.AFTER_PREFIXES)
        assert map(lambda x: x[2:], diff_after_lines) == after_contents
        after_indices = get_indices_by_prefix(diff_before_lines, FileDiff.ADDED)

        return before_indices, after_indices


    def __repr__(self):
        return self.file_name

