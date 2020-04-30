import git
import os
from subprocess import Popen

class Repo(object):
    #REPO_DIR = r"C:\Temp\apache_repos"
    REPO_DIR = r"Z:\ev_repos"
    GITHUB_PATH = r"https://github.com/apache/{0}.git"
    JIRA_PATH = r"http:\issues.apache.org\jira\projects\{0}"

    def __init__(self, jira_key, github_name, local_path=None, commit_to_checkout=None):
        self.jira_key = jira_key
        self.github_name = github_name
        if local_path:
            self.local_path = local_path
        else:
            self.local_path = os.path.join(Repo.REPO_DIR, jira_key)
        self.clone_if_needed()
        if commit_to_checkout:
            git.Repo(self.local_path).checkout(commit_to_checkout)

    def clone_if_needed(self):
        try:
            if self.jira_key == 'SB':
                return
            if not os.path.exists(self.local_path):
                Popen("git clone https://github.com/apache/{0}.git {1}".format(self.github_name, self.local_path)).communicate()
        except:
            pass

    def get_github_jira(self):
        return "{0} {1}".format(Repo.GITHUB_PATH.format(self.github_name), Repo.JIRA_PATH.format(self.jira_key))
