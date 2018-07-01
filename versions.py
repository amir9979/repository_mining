import git
from commit import Commit

class Version(object):
    def __init__(self, git_tag):
        self._commit = Commit(git_tag.commit, 0)
        self._name = git_tag.name


def get_repo_versions(repo_path):
    repo = git.Repo(repo_path)
    return map(lambda tag: Version(tag), repo.tags)


def get_tag_by_name(repo_path, tag_name):
    return filter(lambda tag: tag._name == tag_name, get_repo_versions(repo_path))[0]