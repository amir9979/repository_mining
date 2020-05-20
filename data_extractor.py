import os
import re
from datetime import datetime
from functools import reduce
from itertools import product

import git
import pandas as pd
import numpy as np

from commit import Commit
from config import Config
from fixing_issues import VersionInfo
from issues import get_jira_issues
from version_selector import ConfigurationSelectVersion, BinSelectVersion, QuadraticSelectVersion
from versions import Version
from caching import REPOSITORY_DATA_DIR, assert_dir_exists
from repo import Repo


class DataExtractor(object):

    def __init__(self, project):
        self.git_path = project.path()
        self.github_name = project.github()
        self.jira_url = Config().config['REPO']['JiraURL']
        self.jira_project_name = project.jira()
        self.repo = Repo(self.jira_project_name, self.github_name, local_path=self.git_path)

        self.commits = self._get_repo_commits()
        self.versions = self._get_repo_versions()
        self.bugged_files_between_versions = self._get_bugged_files_between_versions()

    def _get_repo_commits(self):
        repo = git.Repo(self.git_path)
        issues = list(map(lambda x: x.key.strip(),
                     filter(lambda issue: issue.type == 'bug', get_jira_issues(self.jira_project_name, self.jira_url))))
        commits = DataExtractor._commits_and_issues(repo, issues)
        return commits

    def _get_repo_versions(self):
        repo = git.Repo(self.git_path)
        tags = zip(list(repo.tags)[1:], list(repo.tags))
        versions = list(map(lambda tag: Version(tag[0], DataExtractor._version_files(tag[0], tag[1])),
                            tags))
        return versions

    def _get_bugged_files_between_versions(self):
        tags_commits = self._get_commits_between_versions()
        tags = []
        for tag in tags_commits:
            if tags_commits[tag]:
                tags.append(VersionInfo(tag, tags_commits[tag]))
        return sorted(tags, key=lambda x: x.version._commit._commit_date)

    def extract(self):
        tags = self.bugged_files_between_versions
        self._store_commited_files()
        self._store_commits()
        self._store_versions(tags)
        self._store_versions_infos(tags)
        self._store_files(tags)

    def _store_commited_files(self):
        columns = ["file_name", "commit_id", "bug_id", "commit_date"]
        commited_files = list(map(lambda c:
                                  list(map(lambda file_name:
                                           [file_name, c._commit_id,
                                            c._bug_id, c._commit_date],
                                    c._files)), self.commits))

        commited_files = reduce(list.__add__, commited_files, [])
        df = pd.DataFrame(commited_files, columns=columns)
        commited_files_dir = self._get_caching_path("CommittedFiles")
        path = os.path.join(commited_files_dir, self.jira_project_name + ".csv")
        df.to_csv(path, index=False)

    def _store_commits(self):
        columns = ["commit_id", "bug_id", "commit_date"]
        commits = [map(lambda c: [c._commit_id, c._bug_id, c._commit_date], self.commits)]
        df = pd.DataFrame(commits, columns=columns)
        commits_dir = self._get_caching_path("Commits")
        path = os.path.join(commits_dir, self.jira_project_name + ".csv")
        df.to_csv(path, index=False)

    def _store_versions(self, tags):
        columns = ["version_name", "#commited_files_in_version", "#bugged_files_in_version", "bugged_ratio",
                   "#commits", "#bugged_commits", "#ratio_bugged_commits", "version_date"]
        df = pd.DataFrame(columns=columns)
        for tag in tags:
            version = {"version_name": tag.version._name,
                       "#commited_files_in_version": len(tag.version_files),
                       "#bugged_files_in_version": len(tag.bugged_files),
                       "bugged_ratio": tag.bugged_ratio,
                       "#commits": tag.num_commits,
                       "#bugged_commits": tag.num_bugged_commits,
                       "#ratio_bugged_commits": tag.ratio_bugged_commits,
                       "version_date": datetime.fromtimestamp(tag.version._commit._commit_date).strftime("%Y-%m-%d")}
            df = df.append(version, ignore_index=True)

        versions_dir = self._get_caching_path("Versions")
        path = os.path.join(versions_dir, self.jira_project_name + ".csv")
        df.to_csv(path, index=False)

    def _store_versions_infos(self, tags):
        versions_infos_dir = os.path.join(self._get_caching_path("VersionsInfos"), self.jira_project_name)
        Config.assert_dir_exists(versions_infos_dir)
        for tag in tags:
            df = pd.DataFrame(tag.commits_shas, columns=["commit_id", "is_buggy"])
            path = os.path.join(versions_infos_dir, tag.version._name + ".csv")
            df.to_csv(path, index=False)

    def _store_files(self, tags):
        files_dir = os.path.join(self._get_caching_path("Files"), self.jira_project_name)
        Config.assert_dir_exists(files_dir)
        for tag in tags:
            files = {file_name: False for file_name in tag.version_files}
            files.update({file_name: True for file_name in tag.bugged_files})
            df = pd.DataFrame(files.items(), columns=["file_name", "is_buggy"])
            path = os.path.join(files_dir, tag.version._name + ".csv")
            df.to_csv(path, index=False)

    def _get_commits_between_versions(self):
        sorted_versions = sorted(self.versions, key=lambda version: version._commit._commit_date)
        sorted_commits_and_versions = sorted(self.versions + self.commits,
                                             key=lambda version: version._commit._commit_date if hasattr(version,
                                                                                                         "_commit") else version._commit_date)
        versions_indices = list(map(lambda version: (version, sorted_commits_and_versions.index(version)), sorted_versions))
        selected_versions = list(filter(lambda vers: vers[0][1] < vers[1][1], zip(versions_indices, versions_indices[1:])))
        return dict(
            map(lambda vers: (vers[0][0], sorted_commits_and_versions[vers[0][1] + 1: vers[1][1]]), selected_versions))

    def _get_caching_path(self, config_name):
        config = Config().config
        file_name = config['DATA_EXTRACTION'][config_name]
        repository_data = config["CACHING"]["RepositoryData"]
        path = os.path.join(repository_data, file_name, self.github_name)
        Config.assert_dir_exists(path)
        return path

    @staticmethod
    def _version_files(new_tag, prev_tag):
        return list(map(lambda diff: diff.b_path, new_tag.commit.tree.diff(prev_tag.commit.tree)))


    @staticmethod
    def _clean_commit_message(commit_message):
        if "git-svn-id" in commit_message:
            return commit_message.split("git-svn-id")[0]
        return commit_message

    @staticmethod
    def _commits_and_issues(repo, issues):
        def replace(chars_to_replace, replacement, s):
            temp_s = s
            for c in chars_to_replace:
                temp_s = temp_s.replace(c, replacement)
            return temp_s

        def get_bug_num_from_comit_text(commit_text, issues_ids):
            text = replace("[]?#,:(){}", "", commit_text.lower())
            text = replace("-_", " ", text)
            for word in text.split():
                if word.isdigit():
                    if word in issues_ids:
                        return word
            return "0"

        commits = []
        issues_ids = list(map(lambda issue: issue.split("-")[1], issues))
        for git_commit in repo.iter_commits():
            try:
                commit_text = DataExtractor._clean_commit_message(git_commit.summary)
            except:
                continue
            commits.append(
                Commit.init_commit_by_git_commit(git_commit, get_bug_num_from_comit_text(commit_text, issues_ids)))
        return commits

    def choose_versions(self, repo=None, version_num=5, configurations=False, bin=True):
        tags = self.bugged_files_between_versions
        if repo is None:
            repo = self.repo

        selector = None
        if configurations:
            selector = ConfigurationSelectVersion(repo, tags, self.versions, version_num)
        else:
            if bin:
                selector = BinSelectVersion(repo, tags, self.versions, version_num)
            else:
                selector = QuadraticSelectVersion(repo, tags, self.versions, version_num)

        selector.select()
