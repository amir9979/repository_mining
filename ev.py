from apache_repos import find_repo_and_jira
import jira
import github3
from collections import Counter


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
    return map(lambda key: find_repo_and_jira(key, repos, jira_projects), filter(lambda x: x != "SB", jira_and_github))


get_apache_repos_data()
exit()