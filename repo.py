import os

import git

from config import Config


class Repo(object):

    def __init__(self, project, commit_to_checkout=None):
        self.project = project
        if not hasattr(project, 'github_user'):
            github_user_name = "apache"
        else:
            github_user_name = self.project.github_user
        github_path = os.path.join(Config().config['REPO']['GithubPath'], github_user_name)
        self.clone_if_needed(github_path)
        if commit_to_checkout:
            git.Repo(self.project.path).git.checkout(commit_to_checkout.replace('\\', '/'), force=True)

    def clone_if_needed(self, github_path):
        if not os.path.exists(self.project.path):
            git_path = os.path.join(github_path, self.project.github_name + ".git")
            repo = git.Repo.clone_from(git_path, self.project.path)
            print("number of commits: ", len(list(repo.iter_commits())))
            print("number of tags: ", len(list(repo.tags)))
