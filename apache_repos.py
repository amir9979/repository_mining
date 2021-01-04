import jira
import bugzilla
import github3
import os


def get_jira_names(j):
    key = j.key.strip().lower()
    name = j.name.lower().replace('apache','').strip()
    connected_name = "-".join(j.name.strip().lower().split())
    elem = connected_name if '-' not in connected_name else "-".join(connected_name.split('-')[1:])
    return tuple(list(set([key, name, connected_name, elem])))


def get_bz_names(b):
    name = b['name'].lower().replace(' - now in jira', '').replace('apache ', '')
    base_name = name.replace('-', ' ').split()[0]
    return tuple(list(set([name, base_name])))


def get_github_names(g):
    name = g.as_dict()['name'].strip().lower()
    elem = name if '-' not in name else "-".join(name.split('-')[1:])
    return tuple(list(set([name, elem])))


def match_as_project(g, j, bz, github_user, jira_url, bz_url):
    def get_description(g):
        d = g.repository.as_dict().get('description')
        if d:
            return d.encode('utf-8').decode("utf-8").replace('"', '').replace("'", '')
        return ''
    g_name = g.repository.as_dict()['name']
    name = g_name.replace('-', '').replace('.', '')
    g_desc = get_description(g)
    jira_keys = str(list(set(map(lambda x: x.key, j))))
    bz_keys = str(list(set(map(lambda x: x['name'], bz))))
    return f"{name} = Project('{g_name}', '{github_user}', '{g_desc}', {jira_keys}, {bz_keys}, '{jira_url}', '{bz_url}')"


# @cached("apache_repos_data")
def get_repos_data(user='apache', jira_url=r"http://issues.apache.org/jira", bz_url=r"bz.apache.org/bugzilla/xmlrpc.cgi"):
    gh = github3.login(token=os.environ['GITHUB_TOKEN']) # DebuggerIssuesReport@mail.com
    repos = list(gh.search_repositories('org:{0} language:Java'.format(user)))
    bz_products = dict()
    if bz_url:
        bzapi = bugzilla.Bugzilla(bz_url)
        bz_products = dict(map(lambda bz: (get_bz_names(bz), bz), bzapi.getproducts()))
    jira_projects = dict()
    if jira_url:
        jira_projects = dict(map(lambda j: (get_jira_names(j), j), jira.JIRA(jira_url).projects()))

    for r in repos:
        bz_matches = []
        j_matches = []
        for g_name in get_github_names(r):
            for bz in bz_products:
                if g_name in bz:
                    bz_matches.append(bz_products[bz])
                    continue
            for j in jira_projects:
                if g_name in j:
                    j_matches.append(jira_projects[j])
                    continue
        if j_matches or bz_matches:
            print(match_as_project(r, j_matches, bz_matches, user, jira_url, bz_url))


if __name__ == "__main__":
    # get_repos_data('eclipse-cdt', None, "bugs.eclipse.org/bugs/xmlrpc.cgi")
    get_repos_data('spring-projects', "https://jira.spring.io", None)
    # get_repos_data('spring-projects', r"http://jira.spring.io")