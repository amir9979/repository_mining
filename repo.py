import os

import git

from config import Config


class Repo(object):
    config = Config().config

    REPO_DIR = config['REPO']['RepoDir']
    GITHUB_PATH = config['REPO']['GithubPath']
    JIRA_PATH = os.path.join(config['REPO']['JiraURL'], "projects")

    def __init__(self, jira_key, github_name, local_path=None, github_user_name=None, commit_to_checkout=None):
        self.jira_key = jira_key
        self.github_name = github_name
        if local_path:
            self.local_path = local_path
        else:
            self.local_path = os.path.join(Repo.REPO_DIR, jira_key)
        if github_user_name is None:
            github_user_name = "apache"
        github_path = os.path.join(Config().config['REPO']['GithubPath'], github_user_name)
        self.clone_if_needed(github_path)
        if commit_to_checkout:
            git.Repo(local_path).git.checkout(commit_to_checkout, force=True)

    def clone_if_needed(self, github_path):
        if not os.path.exists(self.local_path):
            git_path = os.path.join(github_path, self.github_name + ".git")
            repo = git.Repo.clone_from(git_path, self.local_path)
            print("number of commits: ", len(list(repo.iter_commits())))
            print("number of tags: ", len(list(repo.tags)))

    def get_github_jira(self):
        return "{0} {1}".format(Repo.GITHUB_PATH.format(self.github_name), Repo.JIRA_PATH.format(self.jira_key))
