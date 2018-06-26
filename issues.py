import jira

def get_jira_issues(url, project_name, bunch = 100):
    jira_conn = jira.JIRA(url)
    all_issues=[]
    extracted_issues = 0
    while True:
        issues = jira_conn.search_issues("project={0}".format(project_name), maxResults=bunch, startAt=extracted_issues)
        all_issues.extend(issues)
        extracted_issues=extracted_issues+bunch
        if len(issues) < bunch:
            break
    return all_issues