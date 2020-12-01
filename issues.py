import jira
from caching import cached
import time
import os


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
        except:
            sleep_time = sleep_time * 2
            time.sleep(sleep_time)
    return list(map(lambda issue: Issue(issue, url), all_issues))


if __name__ == "__main__":
    import sys
    from projects import ProjectName
    p = ProjectName[sys.argv[1]]
    get_jira_issues(p.value.jira())