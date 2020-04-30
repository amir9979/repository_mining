
class VersionInfo(object):
    def __init__(self, version, commits):
        self.version = version
        self.commits_shas = list(map(lambda commit: (commit._commit_id, commit._bug_id != "0"), commits))
        self.num_commits = len(commits)
        bugged_commits = filter(lambda commit: commit._bug_id != "0", commits)
        self.num_bugged_commits = len(bugged_commits)
        self.version_files = set(VersionInfo.filter_java_files(self.version.files))
        self.bugged_files = self.version_files.intersection(self.get_commits_files(bugged_commits))
        self.bugged_ratio = 0
        if len(self.version_files) != 0:
            self.bugged_ratio = 1.0 * len(self.bugged_files) / len(self.version_files)
        self.ratio_bugged_commits = 0
        if self.num_commits:
            self.ratio_bugged_commits = 1.0 * self.num_bugged_commits / self.num_commits

    @staticmethod
    def get_commits_files(commits):
        return set(VersionInfo.filter_java_files(reduce(list.__add__, map(lambda commit: commit._files, commits), [])))

    @staticmethod
    def filter_java_files(files):
        return list(filter(lambda x: x.endswith(".java"), files))

