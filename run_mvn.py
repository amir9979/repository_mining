import os
import glob
from junitparser import JUnitXml, junitparser
from junitparser.junitparser import Error, Failure
from subprocess import Popen
import sys
import csv
import xml.etree.ElementTree
import tempfile
csv.field_size_limit(sys.maxsize)

SURFIRE_DIR_NAME = 'surefire-reports'
OBSERVE_PATH = r"c:\temp\observe"


class Test(object):
    def __init__(self, junit_test):
        self.junit_test = junit_test
        self.classname = junit_test.classname
        self.name = junit_test.name
        self.full_name = "{classname}@{name}".format(classname=self.classname, name=self.name).lower()
        result = 'pass'
        if type(junit_test.result) is Error:
            result = 'error'
        if type(junit_test.result) is Failure:
            result = 'failure'
        self.outcome = result

    def __repr__(self):
        return "{full_name}: {outcome}".format(full_name=self.full_name, outcome=self.outcome)

class Trace(object):
    def __init__(self, test_name, trace):
        self.test_name = test_name
        self.trace = trace

    def files_trace(self):
        return list(set(map(lambda x: x.split("@")[0],self.trace)))

class TestRunner(object):
    def __init__(self, git_path, tracer_path=None):
        self.git_path = git_path
        self.tracer_path = tracer_path
        self.observations = {}
        self.traces = {}

    def run(self):
        if self.tracer_path:
            self.trace_tests()
        # self.run_mvn()
        self.observations = self.observe_tests()
        self.collect_traces()

    def run_mvn(self):
        os.system(r'mvn install -fn  -f {0}'.format(self.git_path))

    def trace_tests(self):
        poms = []
        for root, _, files in os.walk(self.git_path):
            poms.extend(map(lambda name: os.path.join(root, name), filter(lambda name: name == "pom.xml", files)))
        map(self.fix_pom_file, poms)

    def fix_pom_file(self, pom_path):
        xml.etree.ElementTree.register_namespace('', "http://maven.apache.org/POM/4.0.0")
        xml.etree.ElementTree.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

        def get_children_by_name(element, name):
            return filter(lambda e: e.tag.endswith(name), element.getchildren())

        def get_or_create_child(element, name):
            child = get_children_by_name(element, name)
            if len(child) == 0:
                return xml.etree.ElementTree.SubElement(element, name)
            else:
                return child[0]

        et = xml.etree.ElementTree.parse(pom_path)
        surfire_plugins = filter(lambda plugin: filter(lambda x: x.text == "maven-surefire-plugin",
                                                       get_children_by_name(plugin, "artifactId")),
                                 filter(lambda e: e.tag.endswith('plugin'), et.getroot().iter()))
        trace_text = self.get_tracer_arg_line()
        for plugin in surfire_plugins:
            configuration = get_or_create_child(plugin, 'configuration')
            argLine = get_or_create_child(configuration, 'argLine')
            argLine.text = argLine.text + trace_text if argLine.text else trace_text
        et.write(pom_path, xml_declaration=True)

    def get_tracer_arg_line(self):
        paths = [os.path.expandvars(r'%USERPROFILE%\.m2\repository'), self.git_path]
        temp_path = tempfile.mktemp()
        with open(temp_path, 'wb') as paths_file:
            paths_file.write("\n".join(paths))
        return ' -javaagent:{0}={1} '.format(self.tracer_path, temp_path)


    def observe_tests(self):
        outcomes = {}
        for report in self.get_surefire_files():
            try:
                for case in JUnitXml.fromfile(report):
                    test = Test(case)
                    outcomes[test.full_name] = (test)
            except:
                pass
        return outcomes

    def get_surefire_files(self):
        surefire_files = []
        for root, _, files in os.walk(self.git_path):
            for name in files:
                if name.endswith('.xml') and os.path.basename(root) == SURFIRE_DIR_NAME:
                    surefire_files.append(os.path.join(root, name))
        return surefire_files

    def collect_traces(self):
        traces_files = []
        for root, dirs, _ in os.walk(os.path.abspath(os.path.join(self.git_path, "..\.."))):
            traces_files.extend(map(lambda name: glob.glob(os.path.join(root, name, "TRACE_*.txt")), filter(lambda name: name == "DebuggerTests", dirs)))
        for trace_file in reduce(list.__add__, traces_files, []):
            test_name = trace_file.split('\\Trace_')[1].split('_')[0].lower()
            with open(trace_file) as f:
                self.traces[test_name] = Trace(test_name, map(lambda line: line.strip().split()[2].strip(), f.readlines()))


def run_mvn_on_commits(commits, git_path):
    for commit in commits:
        observe_tests(commit, git_path)

def checkout_commit(commit_to_observe, git_path):
    git_commit_path = os.path.join(OBSERVE_PATH, os.path.basename(git_path), commit_to_observe)
    Popen(['git', 'clone', git_path, git_commit_path]).communicate()
    Popen(['git', 'checkout', '-f', '{0}'.format(commit_to_observe)], cwd=git_commit_path).communicate()
    return git_commit_path


if __name__ == "__main__":
    # tr = TestRunner(r"C:\Temp\accumulo", r"C:\Users\User\Documents\GitHub\java_tracer\tracer\target\uber-tracer-1.0.1-SNAPSHOT.jar")
    tr = TestRunner(r"C:\Temp\tik\tik\tika", r"C:\Users\User\Documents\GitHub\java_tracer\tracer\target\uber-tracer-1.0.1-SNAPSHOT.jar")
    tr.run()
    from sfl_diagnoser.Diagnoser.diagnoserUtils import write_planning_file
    tests_details = map(lambda test_name: (test_name, tr.traces[test_name].files_trace(), 0 if 'pass' == tr.observations[test_name].outcome else 1), set(tr.traces.keys()) & set(tr.observations.keys()))
    write_planning_file(r'c:\temp\tracer_matrix.txt', [], tests_details)