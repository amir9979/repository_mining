from diff.filediff import FileDiff


class CommitsDiff(object):
    def __init__(self, commit_a, commit_b):
        self.diffs = map(FileDiff,  commit_a.tree.diff(commit_b.tree))


if __name__ == "__main__":
    import git
    repo = git.Repo(r'c:\temp\tika')
    commits = list(repo.iter_commits())
    for i in range(100, 2000):
        CommitsDiff(commits[i], commits[i+1])
    pass