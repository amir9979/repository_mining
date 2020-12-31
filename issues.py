import jira
from caching import cached
import time
import bugzilla
from datetime import datetime


class Issue(object):
    def __init__(self, issue_id, type, priority, resolution, url, creation_time):
        self.issue_id = issue_id
        self.type = type
        self.priority = priority
        self.resolution = resolution
        self.url = url
        self.creation_time = creation_time

    def to_saveable_dict(self):
        return {'issue_id': self.issue_id, 'type': self.type, 'priority': self.priority, 'resolution': self.resolution,
                'url': self.url, 'creation_time': self.creation_time}

    def to_features_dict(self):
        return {'issue_id': self.issue_id, 'type': self.type, 'priority': self.priority, 'resolution': self.resolution}


class JiraIssue(Issue):
    def __init__(self, issue, base_url):
        super().__init__(issue.key.strip().split('-')[1], issue.fields.issuetype.name.lower(), JiraIssue.get_name_or_default(issue.fields.priority, 'minor'), JiraIssue.get_name_or_default(issue.fields.resolution, 'resolved'), base_url, datetime.strptime(issue.fields.created, "%Y-%m-%dT%H:%M:%S.%f%z"))
        self.fields = {}
        for k, v in dict(issue.fields.__dict__).items():
            if k.startswith("customfield_") or k.startswith("__"):
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

    @staticmethod
    def get_name_or_default(val, default):
        if val:
            return val.name.lower()
        return default

class BZIssue(Issue):
    PRIORITY_DICT = {'P1': 'trivial', 'P2': 'minor', 'P3': 'major', 'P4': 'critical', 'P5': 'blocker'}
    def __init__(self, issue):
        super().__init__(str(issue._rawdata['id']), 'bug', BZIssue.PRIORITY_DICT[issue._rawdata['priority']],
                         issue._rawdata['resolution'].lower(), issue.weburl, issue._rawdata['creation_time'])
        self.fields = {'key' : str(issue._rawdata['id'])}
        for k, v in issue._rawdata.items():
            if type(v) in [str, type(None), type(0), type(0.1)]:
                self.fields[k] = str(v)
            elif type(v) in [list, tuple]:
                lst = []
                for item in v:
                    if type(item) in [str]:
                        lst.append(item)
                self.fields[k] = "@@@".join(lst)
        for k in self.fields:
            self.fields[k] = ' '.join(self.fields[k].split())


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
    return list(map(lambda issue: JiraIssue(issue, url), all_issues))


@cached("bugzilla_issues")
def get_bugzilla_issues(product=None, url="bz.apache.org/bugzilla/xmlrpc.cgi"):
    bzapi = bugzilla.Bugzilla(url)
    bugs = []
    sleep_time = 30
    if product is None:
        products = bzapi.getproducts()
    else:
        products = [product]
    for p in products:
        for component in bzapi.getcomponents(p):
            bugs_ = []
            try:
                bugs_ = bzapi.query(bzapi.build_query(product=p, component=component))
            except Exception as e:
                sleep_time = sleep_time * 2
                if sleep_time >= 480:
                    raise e
                time.sleep(sleep_time)
            bugs.extend(bugs_)
    return list(map(lambda issue: BZIssue(issue), bugs))


@cached("issues")
def get_issues_for_project(project):
    if hasattr(project, 'jira_name'):
        return get_jira_issues(project.jira_name)
    jira_issues = []
    bz_issues = []
    for jira_name in project.jira_names:
        jira_issues.extend(get_jira_issues(jira_name, project.jira_url))
    for bz_name in project.bz_names:
        bz_issues.extend(get_bugzilla_issues(bz_name, project.bz_url))
    return jira_issues + bz_issues


if __name__ == "__main__":
    import sys
    from projects import ProjectName
    p = ProjectName[sys.argv[1]]
    get_issues_for_project(p.value)
