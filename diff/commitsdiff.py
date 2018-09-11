from diff.filediff import FileDiff


class CommitsDiff(object):
    def __init__(self, commit_a, commit_b):
        self.diffs = map(FileDiff,  commit_a._git_commit.tree.diff(commit_b._git_commit.tree))


if __name__ == "__main__":
    import git
    import gc
    from commit import Commit
    repo = git.Repo(r'c:\temp\tika')
    commits = list(repo.iter_commits())
    for i in range(100, 300):
        CommitsDiff(Commit.init_commit_by_git_commit(commits[i],0), Commit.init_commit_by_git_commit(commits[i+1], 0))
    pass