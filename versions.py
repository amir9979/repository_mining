from commit import Commit
from _functools import reduce
import os
try:
    from javadiff.javadiff.SourceFile import SourceFile
except:
    from javadiff.SourceFile import SourceFile


class VersionFile(object):
    def __init__(self, file_name, version, repo):
        self.file_name = file_name
        self.version = version
        self.source = SourceFile(repo.git.show("{0}:{1}".format(self.version, self.file_name)), self.file_name, analyze_source_lines=False)
        self.methods = self.source.methods


class Version(object):
    def __init__(self, git_tag, _files):
        self._commit = Commit.init_commit_by_git_commit(git_tag.commit, files=[git_tag.name])
        self._name = os.path.normpath(git_tag.name)
        self.committed_files = _files
        self.files = set(filter(lambda x: x.endswith(".java"), git_tag.commit.repo.git.ls_tree("-r", "--name-only", git_tag.name).split()))
        self.version_files = None

    def get_version_files(self, repo):
        if self.version_files is None:
            self.version_files = []
            for f in self.files:
                try:
                    self.version_files.append(VersionFile(f, self._name, repo))
                except:
                    pass
        return self.version_files

    def get_version_methods(self, repo):
        self.get_version_files(repo)
        return reduce(list.__add__, list(map(lambda f: list(f.methods.values()), self.version_files)), list())
