from commit import Commit


class Version(object):
    def __init__(self, git_tag, _files):
        self._commit = Commit.init_commit_by_git_commit(git_tag.commit)
        self._name = git_tag.name
        self.committed_files = _files
        self.files = set(git_tag.commit.repo.git.ls_tree("-r", "--name-only", git_tag.name).split())
