from diff.filediff import FileDiff


class CommitsDiff(object):
    def __init__(self, commit_a, commit_b):
        self.diffs = map(FileDiff,  commit_a._git_commit.tree.diff(commit_b._git_commit.tree))