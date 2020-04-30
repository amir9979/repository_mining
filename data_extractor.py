import csv
import json
import os
from datetime import datetime

import git

from commit import Commit
from fixing_issues import VersionInfo
from issues import get_jira_issues
from versions import Version
from caching import REPOSIROTY_DATA_DIR, assert_dir_exists
from repo import Repo


class DataExtractor(object):
    VERSIONS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions")
    VERSIONS_INFOS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions_info")
    COMMITS = os.path.join(REPOSIROTY_DATA_DIR, r"commits_info")
    FILES = os.path.join(REPOSIROTY_DATA_DIR, r"files_info")
    CONFIGRATION_PATH = os.path.join(REPOSIROTY_DATA_DIR, r"configurations")
    assert_dir_exists(COMMITS)
    assert_dir_exists(FILES)
    assert_dir_exists(CONFIGRATION_PATH)
    assert_dir_exists(VERSIONS_INFOS)
    CONFIGRATION = r"""workingDir=C:\amirelm\projects\{WORKING_DIR}
    git={GIT_PATH}
    issue_tracker_product_name={PRODUCT_NAME}
    issue_tracker_url=https://issues.apache.org/jira
    issue_tracker=jira
    vers={VERSIONS}
    """
    assert_dir_exists(VERSIONS)

    def __init__(self, git_path, jira_project_name, jira_url=r"http://issues.apache.org/jira"):
        self.git_path = git_path
        self.jira_url = jira_url
        self.jira_project_name = jira_project_name
        self.commits = []
        self.versions = self.get_repo_versions()

    @staticmethod
    def version_files(key, new_tag, prev_tag):
        return map(lambda diff: diff.b_path, new_tag.commit.tree.diff(prev_tag.commit.tree))

    def get_repo_versions(self):
        repo = git.Repo(self.git_path)
        return map(lambda tag: Version(tag[0], DataExtractor.version_files(tag[0].name, tag[0], tag[1])),
                   zip(repo.tags[1:], repo.tags))

    @staticmethod
    def clean_commit_message(commit_message):
        if "git-svn-id" in commit_message:
            return commit_message.split("git-svn-id")[0]
        return commit_message

    @staticmethod
    def commits_and_issues(repo, issues):
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
        issues_ids = map(lambda issue: issue.split("-")[1], issues)
        for git_commit in repo.iter_commits():
            commit_text = DataExtractor.clean_commit_message(git_commit.summary)
            commits.append(
                Commit.init_commit_by_git_commit(git_commit, get_bug_num_from_comit_text(commit_text, issues_ids)))
        return commits

    def get_commits_between_versions(self):
        sorted_versions = sorted(self.versions, key=lambda version: version._commit._commit_date)
        sorted_commits_and_versions = sorted(self.versions + self.commits,
                                             key=lambda version: version._commit._commit_date if hasattr(version,
                                                                                                         "_commit") else version._commit_date)
        versions_indices = map(lambda version: (version, sorted_commits_and_versions.index(version)), sorted_versions)
        selected_versions = filter(lambda vers: vers[0][1] < vers[1][1], zip(versions_indices, versions_indices[1:]))
        return dict(
            map(lambda vers: (vers[0][0], sorted_commits_and_versions[vers[0][1] + 1: vers[1][1]]), selected_versions))

    # @cached(r"apache_commits_data")
    def get_data(self):
        repo = git.Repo(self.git_path)
        issues = map(lambda x: x.key.strip(),
                     filter(lambda issue: issue.type == 'bug', get_jira_issues(self.jira_project_name, self.jira_url)))
        commits = DataExtractor.commits_and_issues(repo, issues)
        return commits

    def get_bugged_files_between_versions(self):
        self.commits = self.get_data()
        tags_commits = self.get_commits_between_versions()
        tags = []
        for tag in tags_commits:
            if tags_commits[tag]:
                tags.append(VersionInfo(tag, tags_commits[tag]))
        return sorted(tags, key=lambda x: x.version._commit._commit_date)

    def extract(self):
        tags = self.get_bugged_files_between_versions()
        with open(os.path.join(DataExtractor.COMMITS, self.jira_project_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows([["commit_id", "bug_id"]] + map(lambda c: [c._commit_id, c._bug_id], self.commits))
        with open(os.path.join(DataExtractor.VERSIONS, self.jira_project_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(["version_name", "#commited files in version", "#bugged files in version", "bugged_ratio",
                             "#commits", "#bugged_commits", "#ratio_bugged_commits", "version_date"])
            for tag in tags:
                writer.writerow([tag.version._name, len(tag.version_files), tag.bugged_files, tag.bugged_ratio, tag.num_commits,
                                 tag.num_bugged_commits, tag.ratio_bugged_commits,
                                 datetime.fromtimestamp(tag.version._commit._commit_date).strftime("%Y-%m-%d")])
        for tag in tags:
            with open(os.path.join(assert_dir_exists(os.path.join(DataExtractor.VERSIONS_INFOS, self.jira_project_name)), tag.version._name) + ".csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows([["commit_id", "is_buggy"]] + tag.commits_shas)
        for tag in tags:
            with open(os.path.join(assert_dir_exists(os.path.join(DataExtractor.FILES, self.jira_project_name)), tag.version._name) + ".csv", "wb") as f:
                writer = csv.writer(f)
                files = {file_name: False for file_name in tag.version_files}
                files.update({file_name: True for file_name in tag.bugged_files})
                writer.writerows([["file_name", "is_buggy"]] + files.items())

    def get_versions_by_type(self):
        import re
        all_versions = self.versions
        majors = []
        minors = []
        micros = []
        SEPERATORS = ['\.', '\-', '\_']
        template_base = [['([0-9])', '([0-9])([0-9])', '([0-9])$'], ['([0-9])', '([0-9])([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])([0-9])$'], ['([0-9])([0-9])', '([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])$'], ['([0-9])', '([0-9])$']]
        templates = []
        for base in template_base:
            templates.extend(map(lambda sep: sep.join(base), SEPERATORS))
        templates.extend(['([0-9])([0-9])([0-9])$', '([0-9])([0-9])$'])
        for version in all_versions:
            for template in templates:
                values = re.findall(template, version._name)
                if values:
                    values = map(int, values[0])
                    if len(values) == 4:
                        micros.append(version)
                        major, minor1, minor2, micro = values
                        minor = 10 * minor1 + minor2
                    elif len(values) == 3:
                        micros.append(version)
                        major, minor, micro = values
                    else:
                        major, minor = values
                        micro = 0
                    if micro == 0:
                        minors.append(version)
                    if minor == 0 and micro == 0:
                        majors.append(version)
                    break
        return {"all": all_versions, "majors": majors, "minors": minors, "micros": micros}.items()

    def choose_versions(self, repo=None, versions_num=5):
        from itertools import product
        if repo is None:
            repo = Repo(self.jira_project_name, self.jira_project_name, self.git_path)
        for start, stop, step, versions in product([1, 5, 10], [100], [5, 10, 20],
                                                   self.get_versions_by_type()):
            bins = map(lambda x: list(), range(start, stop, step))
            tags = self.get_bugged_files_between_versions()
            for tag in tags:
                bugged_flies = len(filter(lambda x: "java" in x, tag.bugged_files))
                java_files = len(filter(lambda x: "java" in x, tag.version_files))
                if bugged_flies * java_files == 0:
                    continue
                bugged_ratio = 1.0 * bugged_flies / java_files
                bins[int(((bugged_ratio * 100) - start) / step) - 1].append(tag.version._name)
            for ind, bin in enumerate(bins):
                if len(bin) < versions_num:
                    continue
                id = "{0}_{1}_{2}_{3}_{4}_{5}".format(repo.jira_key, start, stop, step, versions[0], ind)
                with open(os.path.join(DataExtractor.CONFIGRATION_PATH, id), "wb") as f:
                    f.write(DataExtractor.CONFIGRATION.format(WORKING_DIR=id, PRODUCT_NAME=repo.jira_key, GIT_PATH=repo.local_path,
                                                VERSIONS=repr(tuple(bin)).replace("'", "")))
