import os
from junitparser import JUnitXml, junitparser
from junitparser.junitparser import Error, Failure
from subprocess import Popen
import sys
import csv
csv.field_size_limit(sys.maxsize)

SURFIRE_DIR_NAME = 'surefire-reports'
OBSERVE_PATH = r"c:\temp\observe"

class Test(object):
    def __init__(self, junit_test):
        self.junit_test = junit_test
        self.classname = junit_test.classname
        self.name = junit_test.name
        result = 'pass'
        if type(junit_test.result) is Error:
            result = 'error'
        if type(junit_test.result) is Failure:
            result = 'failure'
        self.out_come = result

    def __repr__(self):
        return "{classname}@{name}: {outcome}".format(classname=self.classname, name=self.name, outcome=self.outcome)


def get_tests_results(repo_dir):
    surefire_reports = get_surefire_files(repo_dir)
    outcomes = []
    for report in surefire_reports:
        try:
            for case in JUnitXml.fromfile(report):
                outcomes.append(Test(case))
        except:
            pass
    return outcomes


def get_surefire_files(repo_dir):
    surefire_files = []
    for root, _, files in os.walk(repo_dir):
        for name in files:
            if name.endswith('.xml') and os.path.basename(root) == SURFIRE_DIR_NAME:
                surefire_files.append(os.path.join(root, name))
    return surefire_files


def run_mvn_on_commits(commits, git_path):
    for commit in commits:
        observe_tests(commit, git_path)


def observe_tests(commit_to_observe, git_path):
    git_commit_path = checkout_commit(commit_to_observe, git_path)
    add_java_agent_tracer(git_commit_path)
    run_mvn(git_commit_path)
    return get_tests_results(git_commit_path)


def add_java_agent_tracer(git_commit_path):
    poms = []
    for root, _, files in os.walk(git_commit_path):
        poms.extend(map(lambda name: os.path.join(root, name), filter(lambda name: name == "pom.xml", files)))
    map(fix_pom_file, poms)


def fix_pom_file(pom_path):
    pass


def run_mvn(git_commit_path):
    os.system(r'mvn install -fn  -f {0}'.format(git_commit_path))


def checkout_commit(commit_to_observe, git_path):
    git_commit_path = os.path.join(OBSERVE_PATH, os.path.basename(git_path), commit_to_observe)
    Popen(['git', 'clone', git_path, git_commit_path]).communicate()
    Popen(['git', 'checkout', '-f', '{0}'.format(commit_to_observe)], cwd=git_commit_path).communicate()
    return git_commit_path


if __name__ == "__main__":
    commits_file = r"C:\Temp\commits3.csv"
    git_path = r"C:\Temp\example\airavata"
    fixing_issues.main(commits_file, git_path, r"http://issues.apache.org/jira", r"AIRAVATA")
    commits = map(lambda x: x[0], filter(lambda x: x[1] != '0', list(csv.reader(open(commits_file)))))
    run_mvn_on_commits(commits, git_path)
