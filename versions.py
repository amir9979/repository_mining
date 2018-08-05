import git
from commit import Commit
from diff import Diff

class Version(object):
    def __init__(self, repo, git_tag):
        self._commit = Commit(git_tag.commit, 0)
        self._name = git_tag.name
        self.version_files = version_files(repo, git_tag)
        # self.diffs = map(Diff, repo.head.commit.tree.diff(git_tag.commit.tree))

def version_files(repo, tag):
    return map(lambda diff: diff.b_path, repo.head.commit.tree.diff(tag.commit.tree))

def get_repo_versions(repo_path):
    repo = git.Repo(repo_path)
    return map(lambda tag: Version(repo, tag), repo.tags)


def get_tag_by_name(repo_path, tag_name):
    return filter(lambda tag: tag._name == tag_name, get_repo_versions(repo_path))[0]