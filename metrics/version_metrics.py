from caching import REPOSIROTY_DATA_DIR, assert_dir_exists
import os
from javadiff.javadiff.SourceFile import SourceFile
import csv
from subprocess import Popen
import tempfile
from itertools import repeat
from xml.etree import ElementTree
import shutil
import pandas as pd


class VersionMetrcs(object):
    EXTERNALS = os.path.realpath(os.path.join(os.path.dirname(__file__), r"..\externals"))
    METHODS = os.path.join(REPOSIROTY_DATA_DIR, r"methods")
    METRICS = os.path.join(REPOSIROTY_DATA_DIR, r"metrics")
    assert_dir_exists(METHODS)
    assert_dir_exists(METRICS)

    def __init__(self, repo, jira_project_name, version_name):
        self.repo = repo
        self.jira_project_name = jira_project_name
        self.version_name = version_name
        self.methods = []
        self.methods_by_file_line = {}
        self.checkstyle = {}
        self.ck = {}
        self.designite = {}
        self.source_monitor = {}
        self.metrics = {}

    def extract(self):
        self.methods_per_file()
        self.designite_data()
        self.checkstyle_data()
        self.source_monitor_data()
        self.ck_data()
        for m in self.methods_by_file_line.values():
            self.metrics[m] = dict()
            for metric_dict in [self.ck, self.designite, self.source_monitor, self.checkstyle]:
                self.metrics[m].update(metric_dict.get(m))
        keys = ["method_id"] + sorted(self.metrics.items()[0][0])
        with open(os.path.join(assert_dir_exists(os.path.join(VersionMetrcs.METRICS, self.jira_project_name)), self.version_name)+ ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow([keys])
            for m in self.metrics.values():
                writer.writerow(map(lambda k: m.get(k), keys))

    def methods_per_file(self):
        self.methods = []
        self.methods_by_file_line = {}
        for root, dirs, files in os.walk(self.repo.local_path):
            for name in filter(lambda x: x.endswith(".java"), files):
                with open(os.path.join(root, name)) as f:
                    sf = SourceFile(f.read(), os.path.join(root, name)[len(self.repo.local_path)+1:])
                    self.methods.extend(list(sf.methods.values()))
                    self.methods_by_file_line.update(dict(list(map(lambda m: ((m.file_name, m.start_line), m.method_id),
                                                                   list(sf.methods.values())))))
        with open(os.path.join(assert_dir_exists(os.path.join(VersionMetrcs.METHODS, self.jira_project_name)), self.version_name)+ ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows([["method_id", "file_name", "method_name", "start_line", "end_line"]] +
                             map(lambda m: [m.method_id, m.file_name, m.method_name, m.start_line, m.end_line], self.methods))

    def checkstyle_data(self):
        self.checkstyle = {}
        tmp = {}
        keys = set()
        f, path_to_xml = tempfile.mkstemp()
        Popen(["java", "-jar", os.path.join(VersionMetrcs.EXTERNALS, "checkstyle-8.32-all.jar"), "-c",
               os.path.join(VersionMetrcs.EXTERNALS, "allChecks.xml"), "-f", "xml", "-o", path_to_xml, self.repo.jira_key]).communicate()
        files = {}
        with open(path_to_xml) as f:
            for fileElement in ElementTree.parse(f).getroot():
                filepath = fileElement.attrib['name']
                items = []
                for errorElement in fileElement:
                    line = int(errorElement.attrib['line'])
                    if "max allowed" not in errorElement.attrib['message']:
                        continue
                    key = "_".join(
                            errorElement.attrib['message'].replace("lines", "").replace(",", "").split('(')[0].split()[
                            :-2])
                    value = int(
                            errorElement.attrib['message'].replace("lines", "").replace(",", "").split('(')[0].split()[
                                -1].strip())
                    items.append({
                        'line': line,
                        'key': key,
                        'value': value,
                        'file': filepath[len(self.repo.local_path)+1:],
                    })
                    keys.add(key)
                    method_id = self.get_closest_id(filepath, line)
                    if method_id:
                        tmp.setdefault(method_id, dict())[key] = value
                files[filepath] = items
        for method_id in tmp:
            self.checkstyle[method_id] = dict.fromkeys(keys, 0)
            self.checkstyle[method_id].update(tmp[method_id])
        os.remove(path_to_xml)

    def source_monitor_data(self):
        out_dir = tempfile.mkdtemp()
        xml = """
            <!--?xml version="1.0" encoding="UTF-8" ?-->
        <sourcemonitor_commands>

           <write_log>true</write_log>

           <command>
               <project_file>verP.smp</project_file>
               <project_language>Java</project_language>
               <file_extensions>*.java</file_extensions>
               <source_directory>verREPO</source_directory>
               <include_subdirectories>true</include_subdirectories>
               <checkpoint_name>Baseline</checkpoint_name>

               <export>
                   <export_file>verP\source_monitor_classes.csv</export_file>
                   <export_type>3 (Export project details in CSV)</export_type>
                   <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
               </export>
           </command>

           <command>
               <project_file>verP.smp</project_file>
               <project_language>Java</project_language>
               <file_extensions>*.java</file_extensions>
               <source_directory>verREPO</source_directory>
               <include_subdirectories>true</include_subdirectories>
               <checkpoint_name>Baseline</checkpoint_name>
               <export>
                   <export_file>verP\source_monitor_methods.csv</export_file>
                   <export_type>6 (Export method metrics in CSV)</export_type>
                   <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
               </export>
           </command>

        </sourcemonitor_commands>""".replace("verP", out_dir).replace("verREPO", self.repo.local_path)
        xmlPath = os.path.join(out_dir, "sourceMonitor.xml")
        with open(xmlPath, "wb") as f:
            f.write(xml)
        Popen([os.path.join(VersionMetrcs.EXTERNALS, "SourceMonitor.exe"), "/C", xmlPath]).communicate()
        # to do : analyze

        shutil.rmtree(out_dir)

    def designite_data(self):
        out_dir = tempfile.mkdtemp()
        Popen([os.path.join(VersionMetrcs.EXTERNALS, "DesigniteJava.jar"), "-i", self.repo.local_path, "-o", out_dir]).communicate()
        # to do : analyze

        shutil.rmtree(out_dir)

    def get_closest_id(self, file_name, line):
        method_id = None
        for l in [line, line + 1, line - 1]:
            if (file_name[len(self.repo.local_path) + 1:], l) in self.methods_by_file_line:
                method_id = self.methods_by_file_line[(file_name[len(self.repo.local_path) + 1:], l)]
                break
        return method_id

    def ck_data(self):
        self.ck = {}
        out_dir = tempfile.mkdtemp()
        Popen([os.path.join(VersionMetrcs.EXTERNALS, "ck-0.5.3-SNAPSHOT-jar-with-dependencies.jar"), self.repo.local_path],
              cwd=out_dir).communicate()
        # to do : analyze
        df = pd.read_csv(os.path.join(out_dir, "method.csv"))
        df = df.drop(['class', "method"], axis=1)
        df['method_id'] = df.apply(lambda x: self.get_closest_id(x['file'], x['line']), axis=1)
        df = df[df['method_id'] is not None]
        df = df.drop(['file', "line"], axis=1)
        df.apply(lambda x: self.ck.setdefault(x["method_id"], x.drop(("method_id"))), axis=1)
        shutil.rmtree(out_dir)

