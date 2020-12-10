import jira
import github3
import os
import csv
import sys
from collections import Counter
from itertools import product
# from data_extractor import DataExtractor
# from caching import cached
# from repo import Repo

REPO_DIR = r"C:\Temp\apache_repos"


def find_repo_and_jira(key, repos, jira_projects):
    def get_description(g):
        d = g.repository.as_dict().get('description')
        if d:
            return d
        return ''
    jira_project = set(filter(lambda p: key in [p.key.strip().lower(), "-".join(p.name.strip().lower().split())], jira_projects))
    github = set(filter(lambda repo: key in repo.as_dict()['name'].strip().lower(), repos))
    for g, j in product(github, jira_project):
        yield "{1} = Project({0}, {1}, {2})".format(g.repository.as_dict()['name'], j.key, get_description(g).encode('utf-8'))

# @cached("apache_repos_data")
def get_repos_data(user='apache', jira_url=r"http://issues.apache.org/jira"):
    gh = github3.login(token=os.environ['GITHUB_TOKEN']) # DebuggerIssuesReport@mail.com
    repos = list(gh.search_repositories('org:{0} language:Java'.format(user)))
    conn = jira.JIRA(jira_url)
    jira_projects = conn.projects()
    github_repos = list(map(lambda repo: repo.as_dict()['name'].strip().lower(), repos))
    _repos = list(map(lambda x: x if '-' not in x else "-".join(x.split('-')[1:]), github_repos))
    jira_keys = list(map(lambda p: p.key.strip().lower(), jira_projects))
    jira_names = list(map(lambda p: "-".join(p.name.strip().lower().split()), jira_projects))
    jira_elements = list(set(jira_names + jira_keys))
    _elements = list(map(lambda x: x if '-' not in x else "-".join(x.split('-')[1:]), jira_elements))
    jira_elements = list(set(_elements + jira_elements))
    jira_and_github = list(map(lambda x: x[0], filter(lambda x: x[1] > 1, Counter(list(set(github_repos + _repos)) + jira_elements).most_common())))
    for key in jira_and_github:
        for repo in find_repo_and_jira(key, repos, jira_projects):
            if repo:
                print(repo)


if __name__ == "__main__":
    get_repos_data('spring-projects', r"http://jira.spring.io")