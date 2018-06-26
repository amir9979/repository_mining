import os
from junitparser import JUnitXml, junitparser
from junitparser.junitparser import Error, Failure
from subprocess import Popen
import sys
import csv
csv.field_size_limit(sys.maxsize)

SURFIRE_DIR_NAME = 'surefire-reports'

def get_tests_results(repo_dir):
    surefire_reports = get_surefire_files(repo_dir)
    outcomes = {}
    for report in surefire_reports:
		try:
			for case in JUnitXml.fromfile(report):
				result = 'pass'
				if type(case.result) is Error:
					result = 'error'
				if type(case.result) is Failure:
					result = 'failure'
				outcomes["{classname}@{name}".format(classname=case.classname, name=case.name)] = result
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

if __name__ == "__main__":	
	commits = map(lambda x: x[0], filter(lambda x: x[1] != '0',list(csv.reader(open(r"C:\Temp\commits2.csv")))))
	for commit in commits:
		GIT_PATH = r'C:\Temp\example\airavata'
		GIT_COMMIT_PATH = r'C:\Temp\example\airavata_{0}'.format(commit)
		Popen(['git', 'clone', GIT_PATH, GIT_COMMIT_PATH]).communicate()
		Popen(['git', 'checkout', '-f', '{0}~1'.format(commit)], cwd=GIT_COMMIT_PATH).communicate()
		os.system(r'mvn install -fn  -f {0}'.format(GIT_COMMIT_PATH))
		res = get_tests_results(GIT_COMMIT_PATH)
		failed_tests = map(lambda x: x[0], filter(lambda x: x[1] != 'pass' and x[1] != 'error', res.items()))
		with open(r'C:\Temp\example\failed_tests_{0}.txt'.format(commit), 'wb') as f:
			f.writelines(failed_tests)