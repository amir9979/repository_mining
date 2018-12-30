import jira
import github3
import os
import csv
import sys
from collections import Counter
from versions import get_repo_versions, get_tags_by_name
from fixing_issues import save_bugs, get_bugged_files_between_versions
from caching import REPOSIROTY_DATA_DIR, cached, assert_dir_exists

REPO_DIR = r"C:\Temp\apache_repos"
VERSIONS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions")
CONFIGRATION_PATH = os.path.join(REPOSIROTY_DATA_DIR, r"configurations")
assert_dir_exists(CONFIGRATION_PATH)
assert_dir_exists(VERSIONS)
CONFIGRATION = r"""workingDir=C:\amirelm\projects\{WORKING_DIR}
git={GIT_PATH}
issue_tracker_product_name={PRODUCT_NAME}
issue_tracker_url=https://issues.apache.org/jira
issue_tracker=jira
vers=({TAG_1},{TAG_2}, {TAG_3}, {TAG_4},{TAG_5})
"""

def find_repo_and_jira(key, repos, jira_projects):
    jira_project = filter(lambda p: key in [p.key.strip().lower(), "-".join(p.name.strip().lower().split())], jira_projects)[0]
    github = filter(lambda repo: repo.as_dict()['name'].strip().lower() == key, repos)[0]
    return os.path.join(REPO_DIR, github.repository.as_dict()['name']), jira_project.key

@cached("apache_repos_data")
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


def search_for_pom(repo):
    for _, _, files in os.walk(repo):
        if any(map(lambda f: 'pom.xml' in f.lower(), files)):
            return True
        elif any(map(lambda f: 'build.xml' in f.lower(), files)):
            return False
        elif any(map(lambda f: 'gradle' in f.lower(), files)):
            return False
    return False

def sava_bugs_for_project(repo, jira_key):
    if not os.path.exists(repo):
        print "start git clone https://github.com/apache/{0}.git".format(os.path.basename(repo))
    if not "pom.xml" in os.listdir(repo):
        return
    versions = get_repo_versions(repo)
    if len(versions) < 5:
        return
    save_bugs(os.path.join(VERSIONS, jira_key) + ".csv", repo, r"http://issues.apache.org/jira", jira_key, versions)


def create_apache_data():
    repos_and_jira = get_apache_repos_data()
    for repo, jira_key in repos_and_jira:
        sava_bugs_for_project(repo, jira_key)


def choose_versions(repo, jira_key, ind=3):
    versions_file = os.path.join(VERSIONS, jira_key) + ".csv"
    if not os.path.exists(versions_file):
        return
    with open(versions_file) as f:
        lines = list(csv.reader(f))[1:]
        if len(lines) < 6:
            return
        version_names = map(lambda x: x[0], filter(lambda x: 0.3 > float(x[ind]) > 0.07, lines))
        selected_versions = map(lambda vers: get_tags_by_name(repo, vers), map(lambda i: version_names[i:i + 6], range(len(version_names) - 6)))
        for ind, versions in enumerate(selected_versions):
            tags = get_bugged_files_between_versions(repo, r"http://issues.apache.org/jira", jira_key, versions)
            ratios = []
            for tag in tags:
                bugged_flies = len(filter(lambda x: "java" in x, tag.bugged_files))
                java_files = len(filter(lambda x: "java" in x, tag.commited_files))
                bugged_ratio = 1.0 * bugged_flies / java_files
                ratios.append(bugged_ratio)
            if all(map(lambda x: 0.35 > x > 0.07, ratios)):
                with open(os.path.join(CONFIGRATION_PATH, "{0}_{1}".format(jira_key, ind)), "wb") as f:
                    tags_names = map(lambda x: x.tag._name, tags)
                    if len(tags_names) < 5:
                        continue
                    f.write(CONFIGRATION.format(WORKING_DIR="{0}_{1}".format(jira_key, ind), PRODUCT_NAME=jira_key,
                                                GIT_PATH=repo, TAG_1=tags_names[0], TAG_2=tags_names[1],
                                                TAG_3=tags_names[2], TAG_4=tags_names[3], TAG_5=tags_names[4]))


if __name__ == "__main__":
    repos = filter(lambda x: search_for_pom(x[0]), get_apache_repos_data())
    print "\n".join(map(lambda x: "{0}, {1}".format(x[0], x[1]), map(lambda x: (
    os.path.normpath(os.path.join(r'https://github.com/apache', os.path.basename(x[0]))),
    os.path.normpath(os.path.join(r"http://issues.apache.org/jira/projects", x[1]))), repos)))
    if len(sys.argv) == 3:
        repo, jira_key = sys.argv[1:]
        sava_bugs_for_project(repo, jira_key)
        # choose_versions(repo, jira_key)
    else:
        for repo, jira_key in get_apache_repos_data():
            sava_bugs_for_project(repo, jira_key)
            choose_versions(repo, jira_key)



