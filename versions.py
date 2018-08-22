import git
import os
from commit import Commit
from diff import FileDiff
from caching import cached

class Version(object):
    def __init__(self, repo, git_tag):
        self._commit = Commit.init_commit_by_git_commit(git_tag.commit, 0)
        self._name = git_tag.name
        self.version_files = version_files("{0}_{1}".format(os.path.basename(os.path.dirname(repo.git_dir)), git_tag.name), git_tag, repo)
        # self.diffs = map(Diff, repo.head.commit.tree.diff(git_tag.commit.tree))


@cached("version_files")
def version_files(tag_name, tag, repo):
    return map(lambda diff: diff.b_path, repo.head.commit.tree.diff(tag.commit.tree))


def get_repo_versions(repo_path):
    repo = git.Repo(repo_path)
    return map(lambda tag: Version(repo, tag), repo.tags)


def get_tags_by_name(repo_path, tags_names):
    repo_tags = get_repo_versions(repo_path)
    return map(lambda tag_name: filter(lambda tag: tag._name == tag_name, repo_tags)[0], tags_names)


def get_tag_by_name(repo_path, tag_name):
    return get_tags_by_name(repo_path, [tag_name])[0]