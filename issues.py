import jira
from caching import cached
import time
import os
import bugzilla
from datetime import datetime


class Issue(object):
    def __init__(self, issue, base_url):
        self.key = issue.key.strip()
        self.type = issue.fields.issuetype.name.lower()
        self.url = os.path.normpath(os.path.join(base_url, "browse", self.key))
        self.fields = {"key" : self.key}
        for k, v in dict(issue.fields.__dict__).items():
            if k.startswith("customfield_") or k.startswith("__") :
                continue
            if type(v) in [str, type(None), type(0), type(0.1)]:
                self.fields[k] = str(v)
            elif hasattr(v, 'name'):
                self.fields[k] = v.name.replace('\n', '').replace(';', '.,')
            elif type(v) in [list, tuple]:
                lst = []
                for item in v:
                    if type(item) in [str]:
                        lst.append(item)
                    elif hasattr(item, 'name'):
                        lst.append(item.name)
                self.fields[k] = "@@@".join(lst)
        for k in self.fields:
            self.fields[k] = ' '.join(self.fields[k].split())

    def get_creation_time(self):
        return datetime.strptime(self.fields['created'], "%Y-%m-%dT%H:%M:%S.%f%z")


@cached("apache_jira")
def get_jira_issues(project_name, url="http://issues.apache.org/jira", bunch=100):
    jira_conn = jira.JIRA(url)
    all_issues=[]
    extracted_issues = 0
    sleep_time = 30
    while True:
        try:
            issues = jira_conn.search_issues("project={0}".format(project_name), maxResults=bunch, startAt=extracted_issues)
            all_issues.extend(issues)
            extracted_issues=extracted_issues+bunch
            if len(issues) < bunch:
                break
        except Exception as e:
            sleep_time = sleep_time * 2
            if sleep_time >= 480:
                raise e
            time.sleep(sleep_time)
    return list(map(lambda issue: Issue(issue, url), all_issues))

@cached("bugzilla_issues")
def get_bugzilla_issues(product=None, url="bz.apache.org/bugzilla/xmlrpc.cgi"):
    bzapi = bugzilla.Bugzilla(url)
    bugs = []
    if product is None:
        products = bzapi.getproducts()
    else:
        products = [product]
    for p in products:
        for component in bzapi.getcomponents(p):
            bugs.extend(bzapi.query(bzapi.build_query(product=p, component=component)))
    return bugs

@cached("issues")
def get_issues_for_project(project):
    jira_issues = []
    bz_issues = []
    for jira_name in project.jira_names:
        jira_issues.extend(get_jira_issues(jira_name, project.jira_url))
    for bz_name in project.bz_names:
        bz_issues.extend(get_bugzilla_issues(bz_name, project.bz_url))
    return jira_issues + bz_issues