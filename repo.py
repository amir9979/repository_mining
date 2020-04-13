import git
import os
from subprocess import Popen


class Repo(object):
    #REPO_DIR = r"C:\Temp\apache_repos"
    REPO_DIR = r"Z:\ev_repos"

    def __init__(self, jira_key, github_name, local_path=None):
        self.jira_key = jira_key
        self.github_name = github_name
        if local_path:
            self.local_path = local_path
        else:
            self.local_path = os.path.join(Repo.REPO_DIR, jira_key)
        self.clone_if_needed()

    def clone_if_needed(self):
        try:
            if self.jira_key == 'SB':
                return
            if not os.path.exists(self.local_path):
                Popen("git clone https://github.com/apache/{0}.git {1}".format(self.github_name, self.local_path)).communicate()
        except:
            pass
