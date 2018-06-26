
class Commit(object):
    def __init__(self, git_commit, bug_id):
        self._git_commit = git_commit
        self._bug_id = bug_id
        self._commit_id = self._git_commit.hexsha
        self._files = self._git_commit.stats.files.keys()

    def to_list(self):
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]