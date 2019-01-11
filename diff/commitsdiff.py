from diff.filediff import FileDiff
from diff.filediff import SourceFile
from subprocess import Popen, PIPE
import os


class CommitsDiff(object):
    def __init__(self, commit_a, commit_b):
        self.diffs = map(lambda d: FileDiff(d, commit_b.hexsha),  commit_a.tree.diff(commit_b.tree))


class FileHistory(object):
    HISTORY_BY_NAMES = {}

    def __init__(self, source_file):
        self.source_file = source_file
        # recent change will be in lower indices
        self.diff_history = []
        self.methods_implementations = dict.fromkeys(self.source_file.methods.keys())
        assert self.source_file.file_name not in FileHistory.HISTORY_BY_NAMES
        FileHistory.HISTORY_BY_NAMES[self.source_file.file_name] = self

    def add_diff_history(self, diff):
        self.diff_history.append(diff)
        if diff.after_file.file_name in FileHistory.HISTORY_BY_NAMES:
           assert FileHistory.HISTORY_BY_NAMES[diff.after_file.file_name] == self
        if diff.before_file.file_name in FileHistory.HISTORY_BY_NAMES:
           assert FileHistory.HISTORY_BY_NAMES[diff.before_file.file_name] == self
        FileHistory.HISTORY_BY_NAMES[diff.after_file.file_name] = self
        FileHistory.HISTORY_BY_NAMES[diff.before_file.file_name] = self

    @staticmethod
    def add_to_history(diff):
        if diff.after_file.file_name in FileHistory.HISTORY_BY_NAMES:
            FileHistory.HISTORY_BY_NAMES[diff.after_file.file_name].add_diff_history(diff)
        elif diff.before_file.file_name in FileHistory.HISTORY_BY_NAMES:
            FileHistory.HISTORY_BY_NAMES[diff.before_file.file_name].add_diff_history(diff)

    def get_source_methods(self):
        return self.methods_implementations.keys()

    def get_contents(self):
        return self.source_file.contents

    def revert_method(self, method_id):
        found = False
        assert method_id in self.methods_implementations
        start_index = 0
        if self.methods_implementations[method_id] is not None:
            start_index = self.diff_history.index(self.methods_implementations[method_id])
        for i in range(start_index, len(self.diff_history)):
            diff = self.diff_history[i]
            if method_id not in diff.before_file.methods:
                continue
            if diff.before_file.methods[method_id].changed:
                found = True
                self.methods_implementations[method_id] = diff
                self.source_file.replace_method(diff.before_file.methods[method_id])
        return found

    def __repr__(self):
        return self.source_file


if __name__ == "__main__":
    import git
    run_commands = ["git", "ls-files"]
    proc = Popen(run_commands, stdout=PIPE, stderr=PIPE, shell=True, cwd=r'c:\temp\tika')
    out, err = proc.communicate()
    files = []
    for file_name in filter(lambda x: x.endswith(".java"), out.split()):
        contents = []
        with open(os.path.join(r'c:\temp\tika',file_name)) as f:
            contents = f.readlines()
        files.append(FileHistory(SourceFile(contents, [], file_name)))
    repo = git.Repo(r'c:\temp\tika')
    commits = list(repo.iter_commits())
    for i in range(len(commits) - 1)[:100]:
        print i
        commit_diff = CommitsDiff(commits[i], commits[i + 1])
        for file_diff in commit_diff.diffs:
            if file_diff.is_java_file():
                FileHistory.add_to_history(file_diff)
                # FileHistory.HISTORY_BY_NAMES[file_diff.after_file.file_name].revert_method("StringsConfig")
    pass