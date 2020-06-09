import os

import git

from config import Config


class Repo(object):
    config = Config().config

    REPO_DIR = config['REPO']['RepoDir']
    GITHUB_PATH = config['REPO']['GithubPath']
    JIRA_PATH = config['REPO']['JiraPath']

    def __init__(self, jira_key, github_name, local_path=None, commit_to_checkout=None):
        self.jira_key = jira_key
        self.github_name = github_name
        if local_path:
            self.local_path = local_path
        else:
            self.local_path = os.path.join(Repo.REPO_DIR, jira_key)
        self.clone_if_needed()
        if commit_to_checkout:
            git.Repo(local_path).git.checkout(commit_to_checkout, force=True)

    def clone_if_needed(self):
        if self.jira_key == 'SB':
            return
        if not os.path.exists(self.local_path):
            git_path = Config().config['REPO']['GithubPath'].format(self.github_name)
            git.Repo.clone_from(git_path, self.local_path)

    def get_github_jira(self):
        return "{0} {1}".format(Repo.GITHUB_PATH.format(self.github_name), Repo.JIRA_PATH.format(self.jira_key))
