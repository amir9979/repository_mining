import jira
import github3
import os
import csv
import sys
from collections import Counter
from data_extractor import DataExtractor
from caching import cached
from repo import Repo

REPO_DIR = r"C:\Temp\apache_repos"


def find_repo_and_jira(key, repos, jira_projects):
    jira_project = filter(lambda p: key in [p.key.strip().lower(), "-".join(p.name.strip().lower().split())], jira_projects)
    if jira_project:
        jira_project = jira_project[0]
    else:
        return None
    github = filter(lambda repo: repo.as_dict()['name'].strip().lower() == key, repos)
    if github:
        github = github[0]
    else:
        return None
    return Repo(jira_project.key, github.repository.as_dict()['name'])


# @cached("apache_repos_data")
def get_apache_repos_data():
    gh = github3.login('DebuggerIssuesReport', password='DebuggerIssuesReport1') # DebuggerIssuesReport@mail.com
    repos = list(gh.search_repositories('user:apache language:Java'))
    github_repos = map(lambda repo: repo.as_dict()['name'].strip().lower(), repos)
    conn = jira.JIRA(r"http://issues.apache.org/jira")
    jira_projects = conn.projects()
    jira_keys = map(lambda p: p.key.strip().lower(), jira_projects)
    jira_names = map(lambda p: "-".join(p.name.strip().lower().split()), jira_projects)
    jira_elements = list(set(jira_names + jira_keys))
    jira_and_github = map(lambda x: x[0], filter(lambda x: x[1] > 1, Counter(github_repos + jira_elements).most_common()))
    ans = []
    for key in jira_and_github:
        repo = find_repo_and_jira(key, repos, jira_projects)
        if repo:
            ans.append(repo)
    return ans


def search_for_pom(repo):
    for _, _, files in os.walk(repo.local_path):
        if any(map(lambda f: 'pom.xml' in f.lower(), files)):
            return True
        elif any(map(lambda f: 'build.xml' in f.lower(), files)):
            return False
        elif any(map(lambda f: 'gradle' in f.lower(), files)):
            return False
    return False


def save_bugs_for_project(repo):
    d = DataExtractor(repo.local_path, repo.jira_key)
    d.extract()


if __name__ == "__main__":
    # print "\n".join(map(lambda x: "{0}, {1}".format(x[0], x[1]), map(lambda x: (
    # os.path.normpath(os.path.join(r'https://github.com/apache', os.path.basename(x[0]))),
    # os.path.normpath(os.path.join(r"http://issues.apache.org/jira/projects", x[1]))), repos)))
    # repo = Repo(u'KAFKA', u'KAFKA')
    # sava_bugs_for_project(repo)
    # choose_versions(repo)
    #x = get_apache_repos_data()

    if len(sys.argv) == 3:
        r, jira_key = sys.argv[1:]
        repo = Repo(jira_key, jira_key, r)
        save_bugs_for_project(repo)
        #choose_versions(repo)
    else:
        repos = filter(search_for_pom, get_apache_repos_data())
        print map(lambda repo: repo.get_github_jira(), repos)
