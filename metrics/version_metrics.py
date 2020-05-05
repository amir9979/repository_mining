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
from repo import Repo
import time


class VersionMetrics(object):
    EXTERNALS = os.path.realpath(os.path.join(os.path.dirname(__file__), r"..\externals"))
    METHODS = os.path.join(REPOSIROTY_DATA_DIR, r"methods")
    METRICS = os.path.join(REPOSIROTY_DATA_DIR, r"metrics")
    CLASSES_METRICS = os.path.join(REPOSIROTY_DATA_DIR, r"classes_metrics")
    assert_dir_exists(METHODS)
    assert_dir_exists(METRICS)
    assert_dir_exists(CLASSES_METRICS)

    def __init__(self, jira_project_name, local_path, version_name):
        self.repo = Repo(jira_project_name, jira_project_name, local_path, version_name)
        self.jira_project_name = jira_project_name
        self.version_name = version_name
        self.methods = []
        self.methods_by_name = {}
        self.methods_by_file_line = {}
        self.methods_by_path_and_name = {}
        self.classes_paths = {}
        self.checkstyle = {}
        self.ck = {}
        self.designite = {}
        self.designite_classes = {}
        self.source_monitor = {}
        self.source_monitor_files = {}
        self.metrics = {}
        self.files_metrics = {}
        self.classes_metrics = {}

    def extract(self):
        self.methods_per_file()
        self.designite_data()
        self.checkstyle_data()
        self.source_monitor_data()
        self.ck_data()
        for m in self.methods_by_file_line.values():
            self.metrics[m] = dict()
            for metric_dict in [self.ck, self.designite, self.source_monitor, self.checkstyle]:
                self.metrics[m].update(metric_dict.get(m, {}))
        keys = ["method_id"] + sorted(self.metrics.values()[0].keys())
        with open(os.path.join(assert_dir_exists(os.path.join(VersionMetrics.METRICS, self.jira_project_name)), self.version_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(keys)
            for name, m in self.metrics.items():
                writer.writerow([name] + map(lambda k:  m.get(k, 0), keys))

        classes_keys = ["method_id"] + sorted(self.metrics.values()[0].keys())
        with open(os.path.join(assert_dir_exists(os.path.join(VersionMetrics.CLASSES_METRICS, self.jira_project_name)), self.version_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(keys)
            for name, m in self.classes_metrics.items():
                writer.writerow([name] + map(lambda k:  m.get(k, 0), classes_keys))

    def methods_per_file(self):
        """
        Analyses the files and get the classes and methods
        :return:
        """
        self.methods = []
        self.methods_by_file_line = {}
        self.classes_paths = {}
        self.methods_by_name = {}
        self.methods_by_path_and_name = {}
        for root, dirs, files in os.walk(self.repo.local_path):
            for name in filter(lambda x: x.endswith(".java"), files):
                with open(os.path.join(root, name)) as f:
                    sf = SourceFile(f.read(), os.path.join(root, name)[len(self.repo.local_path)+1:])
                    for m in sf.modified_names:
                        self.classes_paths[m.lower()] = sf.file_name.lower()
                    self.methods.extend(list(sf.methods.values()))
                    self.methods_by_file_line.update(dict(list(map(lambda m: ((m.file_name, m.start_line), m.id),
                                                                   list(sf.methods.values())))))
                    self.methods_by_name.update(dict(list(map(lambda m: (m.method_name.lower(), m.id),
                                                                   list(sf.methods.values())))))
                    self.methods_by_path_and_name.update(dict(list(map(lambda m: ((m.file_name.lower(),
                                                                                    (".".join(m.method_name_parameters.lower().split(".")[-2:]))), m.id),
                                                                   list(sf.methods.values())))))
        with open(os.path.join(assert_dir_exists(os.path.join(VersionMetrics.METHODS, self.jira_project_name)), self.version_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows([["method_id", "file_name", "method_name", "start_line", "end_line"]] +
                             map(lambda m: [m.id, m.file_name, m.method_name, m.start_line, m.end_line], self.methods))

    def checkstyle_data(self):
        self.checkstyle = {}
        tmp = {}
        keys = set()
        f, path_to_xml = tempfile.mkstemp()
        p = Popen(["java", "-jar", os.path.join(VersionMetrics.EXTERNALS, "checkstyle-8.32-all.jar"), "-c",
               os.path.join(VersionMetrics.EXTERNALS, "allChecks.xml"), "-f", "xml", "-o", path_to_xml, self.repo.local_path])
        p.communicate()
        p.wait()
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
        time.sleep(1)
        p.kill()
        if os.path.exists(path_to_xml):
            try:
                os.remove(path_to_xml)
            except:
                pass

    def source_monitor_data(self):
        out_dir = tempfile.mkdtemp()
        self.source_monitor = {}
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
        Popen([os.path.join(VersionMetrics.EXTERNALS, "SourceMonitor.exe"), "/C", xmlPath]).communicate()
        # to do : analyze
        files_df = pd.read_csv(os.path.join(out_dir, "source_monitor_classes.csv"))
        cols_to_drop = ["Project Name", "Checkpoint Name", "Created On"]
        for i in cols_to_drop + ['Name of Most Complex Method*']:
            files_df = files_df.drop(i, axis=1)
        files_cols = list(files_df.columns.drop("File Name"))
        self.source_monitor_files = dict(map(lambda x: (x[1]["File Name"], dict(zip(files_cols, list(x[1].drop("File Name"))))), files_df.iterrows()))

        methods_df = pd.read_csv(os.path.join(out_dir, "source_monitor_methods.csv"))
        for i in cols_to_drop:
            methods_df = methods_df.drop(i, axis=1)
        methods_cols = list(methods_df.columns.drop("File Name"))
        self.source_monitor = dict(map(lambda x: (self.methods_by_path_and_name.get((x[1]["File Name"].lower(), x[1]["Method"].lower())),
                                              dict(zip(methods_cols, list(x[1].drop("File Name").drop("Method"))))), methods_df.iterrows()))


        shutil.rmtree(out_dir)

    def designite_data(self):
        out_dir = tempfile.mkdtemp()
        Popen(["java", "-jar", os.path.join(VersionMetrics.EXTERNALS, "DesigniteJava.jar"), "-i", self.repo.local_path, "-o", out_dir]).communicate()
        # to do : analyze
        design_smells_list = [
            'Imperative Abstraction',
            'Multifaceted Abstraction',
            'Unnecessary Abstraction',
            'Unutilized Abstraction',
            'Deficient Encapsulation',
            'Unexploited Encapsulation',
            'Broken Modularization',
            'Cyclic-Dependent Modularization',
            'Insufficient Modularization',
            'Hub-like Modularization',
            'Broken Hierarchy',
            'Cyclic Hierarchy',
            'Deep Hierarchy',
            'Missing Hierarchy',
            'Multipath Hierarchy',
            'Rebellious Hierarchy',
            'Wide Hierarchy']
        design_code_smells = self._designite_smells_helper(os.path.join(out_dir, r"designCodeSmells.csv"),
                                                           ["Package Name", "Type Name"], design_smells_list)
        impl_smells_list = [
            'Abstract Function Call From Constructor',
            'Complex Conditional',
            'Complex Method',
            'Empty catch clause',
            'Long Identifier',
            'Long Method',
            'Long Parameter List',
            'Long Statement',
            'Magic Number',
            'Missing default']
        impl_code_smells = self._designite_smells_helper(os.path.join(out_dir, r"implementationCodeSmells.csv"),
                                                         ["Package Name", "Type Name", "Method Name"], impl_smells_list)

        self.designite_classes.update(design_code_smells)
        self.designite.update(dict(map(lambda x: (self.methods_by_name.get(x[0]), x[1]), impl_code_smells.items())))


        methodMetrics = self._designite_helper(os.path.join(out_dir, r"methodMetrics.csv"), ["Package Name", "Type Name", "MethodName"])
        method_cols = list(methodMetrics.columns.drop("id"))
        self.designite.update(dict(map(lambda x: (self.methods_by_name.get(x[1]["id"]), dict(zip(method_cols, list(x[1].drop("id"))))), methodMetrics.iterrows())))
        classesMetrics = self._designite_helper(os.path.join(out_dir, r"typeMetrics.csv"), ["Package Name", "Type Name"])
        classes_cols = list(classesMetrics.columns.drop("id"))
        self.designite_classes.update(
            dict(map(lambda x: (x[1]["id"], dict(zip(classes_cols, list(x[1].drop("id"))))), classesMetrics.iterrows())))

        shutil.rmtree(out_dir)

    def _designite_helper(self, file_name, ids):
        df = pd.read_csv(file_name)
        df = df.drop(r"Project Name", axis=1)

        df["id"] = df.apply(
            lambda x: ".".join(map(lambda y: x[y], ids)).lower(), axis=1)
        for i in ids:
            df = df.drop(i, axis=1)
        return df

    def _designite_smells_helper(self, file_name, ids, smells):
        implementation_smells = self._designite_helper(file_name, ids)

        smells_for_id = {}
        for id_ in implementation_smells["id"]:
            smells_for_id[id_] = dict.fromkeys(smells, False)
        for line, data in implementation_smells.iterrows():
            smells_for_id[data["id"]][data["Code Smell"]] = True
        return smells_for_id

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
        Popen(["java", "-jar", os.path.join(VersionMetrics.EXTERNALS, "ck-0.5.3-SNAPSHOT-jar-with-dependencies.jar"), self.repo.local_path],
              cwd=out_dir).communicate()
        df = pd.read_csv(os.path.join(out_dir, "method.csv"))
        df = df.drop(['class', "method"], axis=1)
        df['method_id'] = df.apply(lambda x: self.get_closest_id(x['file'], x['line']), axis=1)
        df = df[list(map(lambda x: x is not None, df['method_id'].to_list()))]
        df = df.drop(['file', "line"], axis=1)
        df.apply(lambda x: self.ck.setdefault(x["method_id"], x.drop(("method_id"))), axis=1)
        shutil.rmtree(out_dir)


if __name__ == "__main__":
    v = VersionMetrics("DL", r"C:\temp\DL", "0.3.51-RC1")
    v.extract()
    pass