from functools import reduce


class VersionInfo(object):
    def __init__(self, version, commits, repo, analyze_methods=False):
        self.version = version
        self.commits_shas = list(map(lambda commit: (commit._commit_id, commit.is_bug()), commits))
        self.num_commits = len(commits)
        bugged_commits = list(filter(lambda commit: commit.is_bug(), commits))
        self.num_bugged_commits = len(bugged_commits)
        self.version_files = set(VersionInfo.filter_java_files(self.version.files))
        self.bugged_files = self.version_files.intersection(self.get_commits_files(bugged_commits))
        self.bugged_ratio = 0
        if len(self.version_files) != 0:
            self.bugged_ratio = 1.0 * len(self.bugged_files) / len(self.version_files)
        self.ratio_bugged_commits = 0
        if self.num_commits:
            self.ratio_bugged_commits = 1.0 * self.num_bugged_commits / self.num_commits
        if analyze_methods:
            self.committed_methods = reduce(list.__add__, list(map(lambda c: c.get_commit_methods(), commits)), list())
            self.bugged_methods = list(filter(lambda m: m.changed, self.committed_methods))
            self.version_methods = self.version.get_version_methods(repo)
            self.all_methods = self.committed_methods + self.version_methods
            self.methods_bugged_ratio = 0
            if len(self.all_methods) != 0:
                self.methods_bugged_ratio = 1.0 * len(set(map(lambda m: m.id, self.bugged_methods))) / len(set(map(lambda m: m.id, self.all_methods)))

    @staticmethod
    def get_commits_files(commits):
        return set(VersionInfo.filter_java_files(reduce(list.__add__, map(lambda commit: list(map(lambda x: x.name, commit._files)), commits), [])))

    @staticmethod
    def filter_java_files(files):
        return list(filter(lambda x: x.endswith(".java"), files))

