import git
import os
from commit import Commit
from diff.filediff import FileDiff
from caching import cached

class Version(object):
    def __init__(self, git_tag, _files):
        self._commit = Commit.init_commit_by_git_commit(git_tag.commit, 0)
        self._name = git_tag.name
        self.version_files = _files
        # self.diffs = map(Diff, repo.head.commit.tree.diff(git_tag.commit.tree))


@cached("version_files")
def version_files(new_tag, prev_tag):
    return map(lambda diff: diff.b_path, new_tag.commit.tree.diff(prev_tag.commit.tree))


def get_repo_versions(repo_path):
    repo = git.Repo(repo_path)
    return map(lambda tag: Version(tag[0], version_files(*tag)), zip(repo.tags[1:], repo.tags))


def get_tags_by_name(repo_path, tags_names):
    repo_tags = get_repo_versions(repo_path)
    return map(lambda tag_name: filter(lambda tag: tag._name == tag_name, repo_tags)[0], tags_names)


def get_tag_by_name(repo_path, tag_name):
    return get_tags_by_name(repo_path, [tag_name])[0]