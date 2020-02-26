import git
import csv
import sys
import os
# csv.field_size_limit(sys.maxsize)
from datetime import datetime
from commit import Commit
from versions import get_repo_versions, get_tag_by_name
from issues import get_jira_issues
from caching import cached
from diff.commitsdiff import CommitsDiff
import re

def clean_commit_message(commit_message):
    if "git-svn-id" in commit_message:
        return commit_message.split("git-svn-id")[0]
    return commit_message


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
        commit_text = clean_commit_message(git_commit.summary)
        commits.append(Commit.init_commit_by_git_commit(git_commit, get_bug_num_from_comit_text(commit_text, issues_ids)))
    return commits

@cached(r"apache_commits_data")
def get_data(jira_project_name, jira_url, gitPath):
    repo = git.Repo(gitPath)
    issues = map(lambda x: x.key.strip(), filter(lambda issue: issue.type == 'bug', get_jira_issues(jira_project_name, jira_url)))
    commits = commits_and_issues(repo, issues)
    print jira_project_name, len(issues), len(filter(lambda c: c.is_bug(), commits))
    return commits


def get_commits_between_versions(commits, versions):
    sorted_versions = sorted(versions, key=lambda version: version._commit._commit_date)
    sorted_commits_and_versions = sorted(versions + commits, key=lambda version: version._commit._commit_date if hasattr(version, "_commit") else version._commit_date)
    versions_indices = map(lambda version: (version, sorted_commits_and_versions.index(version)), sorted_versions)
    selected_versions = filter(lambda vers: vers[0][1] < vers[1][1], zip(versions_indices, versions_indices[1:]))
    return dict(map(lambda vers: (vers[0][0], sorted_commits_and_versions[vers[0][1] + 1: vers[1][1]]), selected_versions))


class VersionInfo(object):
    def __init__(self, tag, commits):
        self.tag = tag
        self.tag_files = tag._commit._files
        self.num_commits = len(commits)
        bugged_commits = filter(lambda commit: commit._bug_id != "0", commits)
        self.num_bugged_commits = len(bugged_commits)
        self.commited_files = self.get_commits_files(commits)
        self.bugged_files = self.get_commits_files(bugged_commits)
        # self.commits_diff = self.get_commit_diffs(commits)

    @staticmethod
    def get_commit_diffs(commits):
        return map(lambda commits: CommitsDiff(commits[0], commits[1]), zip(commits, commits[1:]))

    @staticmethod
    def get_commits_files(commits):
        return set(reduce(list.__add__, map(lambda commit: commit._files, commits), []))


def get_bugged_files_between_versions(gitPath, jira_url, jira_project_name, versions):
    commits = get_data(jira_project_name, jira_url, gitPath)
    tags_commits = get_commits_between_versions(commits, versions)
    tags = []
    for tag in tags_commits:
        tags.append(VersionInfo(tag, tags_commits[tag]))
    return sorted(tags, key=lambda x: x.tag._commit._commit_date)


def save_bugs(out_file, gitPath, jira_url, jira_project_name, versions):
    tags = get_bugged_files_between_versions(gitPath, jira_url, jira_project_name, versions)
    with open(out_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(["version_name", "#commited files in version", "#bugged files in version", "bugged_ratio",
                         "#commits", "#bugged_commits", "#ratio_bugged_commits", "version_date"])
        for tag in tags:
            commited_java_files = filter(lambda x: "java" in x, tag.commited_files)
            num_commited_java_files = len(commited_java_files)
            bugged_flies = len(filter(lambda x: "java" in x,  tag.bugged_files))
            bugged_ratio = 0
            if num_commited_java_files != 0:
                bugged_ratio = 1.0 * bugged_flies / num_commited_java_files
            ratio_bugged_commits = 0
            if tag.num_commits:
                ratio_bugged_commits = 1.0 * tag.num_bugged_commits / tag.num_commits
            writer.writerow([tag.tag._name, num_commited_java_files, bugged_flies, bugged_ratio, tag.num_commits,
                             tag.num_bugged_commits, ratio_bugged_commits,
                             datetime.fromtimestamp(tag.tag._commit._commit_date).strftime("%Y-%m-%d")])


def main(out_file, gitPath, jira_url, jira_project_name):
    commits = get_data(jira_project_name, jira_url, gitPath)
    with open(out_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows([c.to_list() for c in commits])


if __name__ == "__main__":
    repo = git.Repo(r"c:\temp\tika")
    versions = get_repo_versions(r"c:\temp\tika")
    tags_commits = get_commits_between_versions(map(lambda c: Commit.init_commit_by_git_commit(c, 0), list(repo.iter_commits())[:1000]), versions)
    tags = []
    for tag in tags_commits:
        tags.append(VersionInfo(tag, tags_commits[tag]))
    import apache_repos
    from caching import REPOSIROTY_DATA_DIR
    VERSIONS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions")
    repos_and_jira = apache_repos.get_apache_repos_data()
    for repo, jira_key in repos_and_jira:
        if not os.path.exists(repo):
            print "start git clone https://github.com/apache/{0}.git".format(os.path.basename(repo))
            continue
        try:
            if os.path.exists(os.path.join(VERSIONS, jira_key) + ".csv"):
                continue
            if not "pom.xml" in os.listdir(repo):
                continue
            versions = get_repo_versions(repo)
            save_bugs(os.path.join(VERSIONS, jira_key) + ".csv", repo, r"http://issues.apache.org/jira", jira_key, versions)
            print repo
        except:
            pass
    # print tags_bugged