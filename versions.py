import git
import os
from commit import Commit
from diff.filediff import FileDiff
from caching import cached


class Version(object):
    def __init__(self, git_tag, _files):
        self._commit = Commit.init_commit_by_git_commit(git_tag.commit, 0)
        self._name = git_tag.name
        self.committed_files = _files
        self.files = set(git_tag.commit.repo.git.ls_tree("-r", "--name-only", git_tag.name).split())
        # self.diffs = map(Diff, repo.head.commit.tree.diff(git_tag.commit.tree))
