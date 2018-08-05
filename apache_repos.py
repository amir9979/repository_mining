import jira
import github3
import os
import csv
from collections import Counter
from versions import get_repo_versions, get_tag_by_name
from fixing_issues import save_bugs, get_bugged_files_between_versions
from caching import REPOSIROTY_DATA_DIR

REPO_DIR = r"C:\Temp\apache_repos"
VERSIONS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions")


def find_repo_and_jira(key, repos, jira_projects):
    jira_project = filter(lambda p: key in [p.key.strip().lower(), "-".join(p.name.strip().lower().split())], jira_projects)[0]
    github = filter(lambda repo: repo.as_dict()['name'].strip().lower() == key, repos)[0]
    return os.path.join(REPO_DIR, github.repository.as_dict()['name']), jira_project.key


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
    return map(lambda key: find_repo_and_jira(key, repos, jira_projects), jira_and_github)


def create_apache_data():
    repos_and_jira = get_apache_repos_data()
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
        except:
            pass


def choose_versions():
    repos_and_jira = get_apache_repos_data()
    for repo, jira_key in repos_and_jira:
        versions_file = os.path.join(VERSIONS, jira_key) + ".csv"
        if not os.path.exists(versions_file):
            continue
        with open(versions_file) as f:
            version_names = map(lambda x: x[0], filter(lambda x: 0.2 > float(x[3]) > 0.1, list(csv.reader(f))[1:]))
            if len(version_names) < 6:
                continue
            selected_versions = map(lambda vers: map(lambda ver: get_tag_by_name(repo, ver), vers), map(lambda i: versions[i:i + 5], range(len(version_names) - 5)))
            for versions in selected_versions:
                tags_bugs = get_bugged_files_between_versions(repo, r"http://issues.apache.org/jira", jira_key, versions)
                ratios = []
                for tag, files in sorted(tags_bugs.items(), key=lambda x: x[0]._commit._commit_date):
                    java_files = len(filter(lambda x: "java" in x, tag.version_files))
                    bugged_fies = len(filter(lambda x: "java" in x, files))
                    bugged_ratio = 1.0 * bugged_fies / java_files
                    ratios.append(bugged_ratio)
                if all(map(lambda x: 0.25 > x > 0.07, ratios)):
                    print repo, jira_key, map(lambda x: x[0]._name, sorted(tags_bugs.items(), key=lambda x: x[0]._commit._commit_date))


if __name__ == "__main__":
    choose_versions()