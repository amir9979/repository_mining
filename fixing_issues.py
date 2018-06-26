import git
import csv
from commit import Commit
from issues import get_jira_issues

def clean_commit_message(commit_message):
    if "git-svn-id" in commit_message:
        return commit_message.split("git-svn-id")[0]
    return commit_message

def commits_and_issues(repo, issues):
    def get_bug_num_from_comit_text(commit_text, issues_ids):

        s = commit_text.lower().replace(":", "").replace("#", "").replace("-", " ").replace("_", " ").split()
        for word in s:
            if word.isdigit():
                if word in issues_ids:
                    return word
        return "0"
    commits= []
    issues_ids = map(lambda issue: issue.key.split("-")[1], issues)
    for git_commit in repo.iter_commits():
        commit_text = clean_commit_message(git_commit.message)
        commits.append(Commit(git_commit, get_bug_num_from_comit_text(commit_text, issues_ids)))
    return commits


def get_data(gitPath, jira_url, jira_project_name):
    repo = git.Repo(gitPath)
    issues = get_jira_issues(jira_url, jira_project_name)
    return commits_and_issues(repo, issues)


def main(out_file, gitPath, jira_url, jira_project_name):
    commits = get_data(gitPath, jira_url, jira_project_name)
    with open(out_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows([c.to_list() for c in commits])

if __name__ == "__main__":
    import sys
    csv.field_size_limit(sys.maxsize)
    main(r"C:\Temp\commits.csv", r"C:\Temp\example\airavata", r"http://issues.apache.org/jira", r"AIRAVATA")