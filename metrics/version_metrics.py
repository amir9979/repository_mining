import os
import time
import csv
from abc import ABC, abstractmethod
from subprocess import Popen
import shutil
import tempfile
import json
from xml.etree import ElementTree
import pdb

import pandas as pd
import click

from caching import cached
from config import Config
from javadiff.javadiff.SourceFile import SourceFile
from metrics.rsc import source_monitor_xml
from metrics.version_metrics_data import Data
from repo import Repo
from .commented_code_detector import metrics_for_project


@click.command()
@click.argument('jira_project_name')
@click.argument('local_path')
@click.argument('version_name')
def main(jira_project_name, local_path, version_name):
    v = VersionMetrics(jira_project_name, local_path, version_name)
    v.extract()
    return


class FileAnalyzer:
    def __init__(self, local_path, project_name, version_name):
        self.local_path = local_path
        cache_name = self._get_cache_name(project_name, version_name)
        analyze = cached(cache_name)(self._analyze)
        res = analyze(local_path)
        self.methods = res[0]
        self._store_methods(project_name, version_name, self.methods)
        self.methods_by_file_line = res[1]
        self.classes_paths = res[2]
        self.methods_by_name = res[3]
        self.methods_by_path_and_name = res[4]

    def get_closest_id(self, file_name, line):
        method_id = None
        for l in [line, line + 1, line - 1]:
            file_path = (file_name[len(self.local_path) + 1:], l)
            if file_path in self.methods_by_file_line:
                method_id = self.methods_by_file_line[(file_name[len(self.local_path) + 1:], l)]
                break
        return method_id

    @staticmethod
    def _get_cache_name(project_name, version_name):
        config = Config().config
        storing_dir = config['VERSION_METRICS']['MethodsDir']
        cache_name = storing_dir + "_" + project_name + "_" + version_name
        return cache_name

    def _analyze(self, local_path):
        methods = []
        methods_by_file_line = {}
        classes_paths = {}
        methods_by_name = {}
        methods_by_path_and_name = {}
        for root, dirs, files in os.walk(local_path):
            for name in filter(lambda x: x.endswith(".java"), files):
                with open(os.path.join(root, name), encoding='latin-1') as f:
                    contents = f.read()
                    file_name = os.path.join(root, name)[len(local_path) + 1:]
                    # TODO Remove print
                    print("Processing: " + file_name)
                    sf = SourceFile(contents, file_name)

                    self._extract_classes(sf, classes_paths)

                    self._extract_methods(sf, methods)

                    self._extract_methods_by_file_line(sf, methods_by_file_line)

                    self._extract_methods_by_name(sf, methods_by_name)

                    self._extract_methods_by_path_and_name(sf, methods_by_path_and_name)

        return methods, methods_by_file_line, classes_paths, methods_by_name, methods_by_path_and_name

    @staticmethod
    def _store_methods(project_name, version_name, methods):
        config = Config().config
        repository_data = Config.get_work_dir_path(config['CACHING']['RepositoryData'])
        out_dir = os.path.join(repository_data, config['VERSION_METRICS']['MethodsDir'], project_name)
        Config.assert_dir_exists(out_dir)
        out_path = os.path.join(out_dir, version_name) + ".csv"
        columns = ["method_id", "file_name", "method_name", "start_line", "end_line"]
        values = list(map(lambda m: [m.id, m.file_name, m.method_name, m.start_line, m.end_line], methods))
        df = pd.DataFrame(values, columns=columns)
        df.to_csv(out_path, index=False)

    @staticmethod
    def _extract_classes(sf, classes_paths):
        for m in sf.modified_names:
            classes_paths[m.lower()] = sf.file_name.lower()

    @staticmethod
    def _extract_methods(sf, methods):
        methods.extend(list(sf.methods.values()))

    @staticmethod
    def _extract_methods_by_file_line(sf, methods_by_file_line):
        methods_by_file_line.update(dict(list(
            map(lambda m: (
                (m.file_name, m.start_line),
                m.id),
                list(sf.methods.values())))))

    @staticmethod
    def _extract_methods_by_name(sf, methods_by_name):
        methods_by_name.update(dict(list(
            map(lambda m: (
                m.method_name.lower(),
                m.id),
                list(sf.methods.values())))))

    @staticmethod
    def _extract_methods_by_path_and_name(sf, methods_by_path_and_name):
        methods_by_path_and_name.update(dict(
            list(
                map(lambda m: (
                    (m.file_name.lower(),
                     (".".join(
                         m.method_name_parameters.lower().split(".")[-2:]))),
                    m.id),
                    list(sf.methods.values()))) +
            list(
                map(lambda m: (
                    (m.file_name.lower(),
                     (".".join(
                         m.method_name.lower().split(".")[-2:]))),
                    m.id),
                    list(sf.methods.values())))))


class Extractor(ABC):
    def __init__(self, extractor_name, project, version):
        self.extractor_name = extractor_name
        self.project = project
        self.version = version
        self.config = Config().config
        self.runner = self._get_runner(self.config, extractor_name)
        self.local_path: str = str()
        self.file_analyzer: FileAnalyzer = FileAnalyzer()
        self.data: Data
        pass

    @staticmethod
    def _get_runner(config, extractor_name):
        externals_path = config['EXTERNALS']['BaseDir']
        runner_name = config['EXTERNALS'][extractor_name]
        externals = Config.get_work_dir_path(externals_path)
        runner = os.path.join(externals, runner_name)
        return runner

    @abstractmethod
    def extract(self, jira_project_name, github_name, local_path):
        repo = Repo(jira_project_name, github_name, local_path, self.version)
        self.local_path = repo.local_path
        self.file_analyzer = FileAnalyzer(self.local_path, self.project, self.version)
        pass


class Checkstyle(Extractor):
    def __init__(self, project, version):
        super().__init__("Checkstyle", project, version)

    def extract(self, jira_project_name, github_name, local_path):
        super(Checkstyle, self).extract(jira_project_name, github_name, local_path)
        all_checks_xml = self._get_all_checks_xml(self.config)
        pdb.set_trace()
        out_path_to_xml = self._execute_command(self.runner, all_checks_xml, self.local_path)
        pdb.set_trace()
        files = {}
        tmp = {}
        keys = set()
        with(open(out_path_to_xml)) as file:
            for file_element in ElementTree.parse(file).getroot():
                filepath = file_element.attrib['name']
                pdb.set_trace()
                items, tmp, keys = self._get_items(file_element, filepath, tmp, keys)
                pdb.set_trace()
                files[filepath] = items

        checkstyle = {}
        for method_id in tmp:
            checkstyle[method_id] = dict.fromkeys(keys, 0)
            checkstyle[method_id].update(tmp[method_id])

        self.data = checkstyle

    @staticmethod
    def _get_all_checks_xml(config):
        externals_path = config['EXTERNALS']['BaseDir']
        all_checks_xml_name = config['EXTERNALS']['AllChecks']
        externals = Config.get_work_dir_path(externals_path)
        all_checks_xml = os.path.join(externals, all_checks_xml_name)
        return all_checks_xml

    @staticmethod
    def _execute_command(checkstyle_runner: str, all_checks_xml: str, local_path: str) -> str:
        f, out_path_to_xml = tempfile.mkstemp()
        commands = ["java",
                    "-jar", checkstyle_runner,
                    "-c", all_checks_xml,
                    "-f", "xml",
                    "-o", out_path_to_xml,
                    local_path]
        p = Popen(commands)
        p.communicate()
        return out_path_to_xml

    def _get_items(self, file_element, file_path, tmp, keys):
        items = []
        for errorElement in file_element:
            line = int(errorElement.attrib['line'])
            if "max allowed" not in errorElement.attrib['message']:
                continue
            key = "_".join(errorElement.attrib['message'] \
                           .replace("lines", "") \
                           .replace(",", "") \
                           .split('(')[0] \
                           .split()[:-2])

            value = int(errorElement.attrib['message'] \
                        .replace("lines", "") \
                        .replace(",", "") \
                        .split('(')[0] \
                        .split()[-1] \
                        .strip())
            items.append({
                'line': line,
                'key': key,
                'value': value,
                'file': file_path[len(self.local_path) + 1:],
            })
            keys.add(key)
            method_id = self.file_analyzer.get_closest_id(file_path, line)
            if method_id:
                tmp.setdefault(method_id, dict())[key] = value
        return file_element, tmp, keys


class Designite(Extractor):
    def extract(self):
        pass


class SourceMonitor(Extractor):
    def __init__(self, project, version):
        super().__init__("SourceMonitor", project, version)

    def extract(self):
        if not os.name == "dt":
            self.data = {}
            return

        out_dir = self._execute_command(self.runner, self.local_path)
        source_monitor_files, source_monitor = self._process_metrics(out_dir)

    @staticmethod
    def _execute_command(source_monitor_runner, local_path):
        out_dir = tempfile.mkdtemp()
        xml = source_monitor_xml.xml \
            .replace("verP", out_dir) \
            .replace("verREPO", local_path)
        xml_path = os.path.join(out_dir, "sourceMonitor.xml")
        with open(xml_path, "wb") as f:
            f.write(xml)

        Popen([source_monitor_runner, "/C", xml_path]).communicate()
        return out_dir

    def _process_metrics(self, out_dir):
        files_path = os.path.join(out_dir, "source_monitor_classes.csv")
        files_df = pd.read_csv(files_path)
        cols_to_drop = ["Project Name", "Checkpoint Name", "Created On"]
        for i in cols_to_drop + ['Name of Most Complex Method*']:
            files_df = files_df.drop(i, axis=1)
        files_cols = list(files_df.columns.drop("File Name"))
        source_monitor_files = dict(
            map(lambda x: (
                x[1]["File Name"],
                dict(zip(files_cols, list(x[1].drop("File Name"))))
            ), files_df.iterrows()))

        methods_path = os.path.join(out_dir, "source_monitor_methods.csv")
        methods_df = pd.read_csv(methods_path)
        for i in cols_to_drop:
            methods_df = methods_df.drop(i, axis=1)
        methods_cols = list(methods_df.columns.drop("File Name"))
        source_monitor = dict(map(lambda x: (
            self._get_source_monitor_id(
                x[1]["File Name"],
                x[1]["Method"],
                self.file_analyzer.methods_by_path_and_name),
            dict(zip(
                methods_cols,
                list(x[1].drop("File Name").drop("Method"))))),
                                  methods_df.iterrows()))
        shutil.rmtree(out_dir)
        return source_monitor_files, source_monitor

    @staticmethod
    def _get_source_monitor_id(source_file_name, source_method, methods_by_path_and_name):
        full_key = (source_file_name.lower(), source_method.lower())
        method_key = (source_file_name.lower(), source_method.lower().split("(")[0])
        extend_key = (
            source_file_name.lower(), source_method.lower().split("<")[0] + "." + source_method.lower().split(".")[1])
        extend_key_params = (source_file_name.lower(),
                             source_method.lower().split("<")[0] + "." + source_method.lower().split(".")[1].split("(")[
                                 0])
        for key in [full_key, method_key, extend_key, extend_key_params]:
            if key in methods_by_path_and_name:
                return methods_by_path_and_name[key]


class CK(Extractor):
    def __init__(self, project, version):
        super().__init__("CK", project, version)

    def extract(self):
        out_dir = self._execute_command(self.runner, self.local_path)
        ck = self._process_metrics(out_dir)
        self.data = ck
        pass

    @staticmethod
    def _execute_command(ck_runner, local_path):
        out_dir = tempfile.mkdtemp()
        command = ["java", "-jar", ck_runner, local_path]
        Popen(command, cwd=out_dir).communicate()
        return out_dir

    def _process_metrics(self, out_dir):
        ck = {}

        df_path = os.path.join(out_dir, "method.csv")
        df = pd.read_csv(df_path)
        df = df.drop(['class', "method"], axis=1)
        df['method_id'] = df.apply(lambda x:
                                   self.file_analyzer.get_closest_id(x['file'], x['line']),
                                   axis=1)
        df = df[list(map(lambda x: x is not None, df['method_id'].to_list()))]
        df = df.drop(['file', "line"], axis=1)
        df.apply(lambda x:
                 ck.setdefault(x["method_id"], x.drop(("method_id"))),
                 axis=1)

        shutil.rmtree(out_dir)
        return ck


class Mood(Extractor):
    def __init__(self, project, version):
        super().__init__("MOOD", project, version)

    def extract(self):
        out_dir = self._execute_command(self.runner, self.local_path)
        mood = self._process_metrics(out_dir)
        self.data = mood

    @staticmethod
    def _execute_command(mood_runner, local_path):
        out_dir = tempfile.mkdtemp()
        command = ["java", "-jar", mood_runner, local_path, out_dir]
        Popen(command).communicate()
        return out_dir

    def _process_metrics(self, out_dir):
        mood = {}
        with open(os.path.join(out_dir, "_metrics.json")) as file:
            mood = dict(map(lambda x: (
                self.file_analyzer.classes_paths.get(x[0].lower()),
                x[1]),
                            json.loads(file.read()).items()))
        shutil.rmtree(out_dir)
        return mood


class Halstead(Extractor):
    def __init__(self, project, version):
        super().__init__("HALSTEAD", project, version)

    def extract(self):
        halstead = metrics_for_project(self.local_path)
        self.data = halstead


class VersionMetrics(object):
    config = Config().config
    # EXTERNALS = os.path.realpath(os.path.join(os.path.dirname(__file__), r"..\externals"))
    externals_path = config['EXTERNALS']['BaseDir']
    EXTERNALS = Config.get_work_dir_path(externals_path)

    # METHODS = os.path.join(REPOSITORY_DATA_DIR, r"methods")
    # METRICS = os.path.join(REPOSITORY_DATA_DIR, r"metrics")
    # CLASSES_METRICS = os.path.join(REPOSITORY_DATA_DIR, r"classes_metrics")
    repository_data = Config.get_work_dir_path(config['CACHING']['RepositoryData'])
    METHODS = os.path.join(repository_data, config['VERSION_METRICS']['MethodsDir'])
    METRICS = os.path.join(repository_data, config['VERSION_METRICS']['MetricsDir'])
    CLASSES_METRICS = os.path.join(repository_data, config['VERSION_METRICS']['ClassesMetricsDir'])

    Config.assert_dir_exists(METHODS)
    Config.assert_dir_exists(METRICS)
    Config.assert_dir_exists(CLASSES_METRICS)

    def __init__(self, jira_project_name, github_name, local_path, version_name):
        self.config = Config().config
        self.repo = Repo(jira_project_name, github_name, local_path, version_name)
        self.jira_project_name = jira_project_name
        self.version_name = version_name
        self.methods = []
        self.methods_by_name = {}
        self.methods_by_file_line = {}
        self.methods_by_path_and_name = {}
        self.classes_paths = {}
        self.checkstyle = {}
        self.ck = {}
        self.halstead = {}
        self.mood = {}
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
        self.mood_data()
        for m in self.methods_by_file_line.values():
            self.metrics[m] = dict()
            for metric_dict in [self.ck, self.designite, self.source_monitor, self.checkstyle]:
                self.metrics[m].update(metric_dict.get(m, {}))
        keys = ["method_id"] + sorted(self.metrics.values()[0].keys())
        with open(os.path.join(Config.assert_dir_exists(os.path.join(VersionMetrics.METRICS, self.jira_project_name)),
                               self.version_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(keys)
            for name, m in self.metrics.items():
                writer.writerow([name] + map(lambda k: m.get(k, 0), keys))

        classes_keys = ["method_id"] + sorted(self.metrics.values()[0].keys())
        with open(os.path.join(
                Config.assert_dir_exists(os.path.join(VersionMetrics.CLASSES_METRICS, self.jira_project_name)),
                self.version_name) + ".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(keys)
            for name, m in self.classes_metrics.items():
                writer.writerow([name] + map(lambda k: m.get(k, 0), classes_keys))

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
                    contents = f.read()
                    file_name = os.path.join(root, name)[len(self.repo.local_path) + 1:]
                    sf = SourceFile(contents, file_name)

                    for m in sf.modified_names:
                        self.classes_paths[m.lower()] = sf.file_name.lower()

                    self.methods.extend(list(sf.methods.values()))

                    self.methods_by_file_line.update(dict(list(
                        map(lambda m: (
                            (m.file_name, m.start_line),
                            m.id),
                            list(sf.methods.values())))))

                    self.methods_by_name.update(dict(list(
                        map(lambda m: (
                            m.method_name.lower(),
                            m.id),
                            list(sf.methods.values())))))

                    self.methods_by_path_and_name.update(dict(
                        list(
                            map(lambda m: (
                                (m.file_name.lower(),
                                 (".".join(
                                     m.method_name_parameters.lower().split(".")[-2:]))),
                                m.id),
                                list(sf.methods.values()))) +
                        list(
                            map(lambda m: (
                                (m.file_name.lower(),
                                 (".".join(
                                     m.method_name.lower().split(".")[-2:]))),
                                m.id),
                                list(sf.methods.values())))))
        out_dir = os.path.join(VersionMetrics.METHODS, self.jira_project_name)
        Config.assert_dir_exists(out_dir)
        out_path = os.path.join(out_dir, self.version_name) + ".csv"
        with open(out_path, "wb") as f:
            writer = csv.writer(f)
            writer.writerows([["method_id", "file_name", "method_name", "start_line", "end_line"]] +
                             map(lambda m: [m.id, m.file_name, m.method_name, m.start_line, m.end_line], self.methods))

    def checkstyle_data(self):
        self.checkstyle = {}
        tmp = {}
        keys = set()
        checkstyle_jar = os.path.join(VersionMetrics.EXTERNALS, self.config['EXTERNALS']['Checkstyle'])
        all_checks_xml = os.path.join(VersionMetrics.EXTERNALS, "allChecks.xml")
        f, path_to_xml = tempfile.mkstemp()
        commands = ["java",
                    "-jar", checkstyle_jar,
                    "-c", all_checks_xml,
                    "-f", "xml",
                    "-o", path_to_xml,
                    self.repo.local_path]
        p = Popen(commands)
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
                    key = "_".join(errorElement.attrib['message'] \
                                   .replace("lines", "") \
                                   .replace(",", "") \
                                   .split('(')[0] \
                                   .split()[:-2])

                    value = int(errorElement.attrib['message'] \
                                .replace("lines", "") \
                                .replace(",", "") \
                                .split('(')[0] \
                                .split()[-1] \
                                .strip())
                    items.append({
                        'line': line,
                        'key': key,
                        'value': value,
                        'file': filepath[len(self.repo.local_path) + 1:],
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
        is_windows_os = os.name == 'nt'
        if not is_windows_os:
            return

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
        xml_path = os.path.join(out_dir, "sourceMonitor.xml")
        with open(xml_path, "wb") as f:
            f.write(xml)

        source_monitor_exe = os.path.join(VersionMetrics.EXTERNALS, self.config["EXTERNALS"]["SourceMonitor"])
        Popen([source_monitor_exe, "/C", xml_path]).communicate()
        # to do : analyze
        files_df = pd.read_csv(os.path.join(out_dir, "source_monitor_classes.csv"))
        cols_to_drop = ["Project Name", "Checkpoint Name", "Created On"]
        for i in cols_to_drop + ['Name of Most Complex Method*']:
            files_df = files_df.drop(i, axis=1)
        files_cols = list(files_df.columns.drop("File Name"))
        self.source_monitor_files = dict(
            map(lambda x: (x[1]["File Name"], dict(zip(files_cols, list(x[1].drop("File Name"))))),
                files_df.iterrows()))

        methods_df = pd.read_csv(os.path.join(out_dir, "source_monitor_methods.csv"))
        for i in cols_to_drop:
            methods_df = methods_df.drop(i, axis=1)
        methods_cols = list(methods_df.columns.drop("File Name"))
        self.source_monitor = dict(map(lambda x: (self.get_source_monitor_id(x[1]["File Name"], x[1]["Method"]),
                                                  dict(zip(methods_cols, list(x[1].drop("File Name").drop("Method"))))),
                                       methods_df.iterrows()))

        shutil.rmtree(out_dir)

    def get_source_monitor_id(self, source_file_name, source_method):
        full_key = (source_file_name.lower(), source_method.lower())
        method_key = (source_file_name.lower(), source_method.lower().split("(")[0])
        extend_key = (
            source_file_name.lower(), source_method.lower().split("<")[0] + "." + source_method.lower().split(".")[1])
        extend_key_params = (source_file_name.lower(),
                             source_method.lower().split("<")[0] + "." + source_method.lower().split(".")[1].split("(")[
                                 0])
        for key in [full_key, method_key, extend_key, extend_key_params]:
            if key in self.methods_by_path_and_name:
                return self.methods_by_path_and_name[key]

    def designite_data(self):
        out_dir = tempfile.mkdtemp()
        designite_jar = os.path.join(VersionMetrics.EXTERNALS, self.config["EXTERNALS"]["DesigniteJava"])
        commands = ["java",
                    "-jar", designite_jar,
                    "-i", self.repo.local_path,
                    "-o", out_dir]

        Popen(commands).communicate()
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
                                                           ["Package Name", "Type Name"],
                                                           design_smells_list)
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
                                                         ["Package Name", "Type Name", "Method Name"],
                                                         impl_smells_list)

        self.designite_classes.update(design_code_smells)
        smells_dict = dict(map(lambda x: (self.methods_by_name.get(x[0]), x[1]), impl_code_smells.items()))

        method_metrics = self._designite_helper(os.path.join(out_dir, r"methodMetrics.csv"),
                                                ["Package Name", "Type Name", "MethodName"])
        method_cols = list(method_metrics.columns.drop("id"))
        methods_metrics_dict = dict(map(lambda x: (
            self.methods_by_name.get(x[1]["id"]),
            dict(zip(method_cols, list(x[1].drop("id"))))
        ), method_metrics.iterrows()))

        classes_metrics = self._designite_helper(os.path.join(out_dir, r"typeMetrics.csv"),
                                                 ["Package Name", "Type Name"])
        classes_cols = list(classes_metrics.columns.drop("id"))
        self.designite_classes.update(
            dict(map(lambda x: (
                x[1]["id"],
                dict(zip(classes_cols, list(x[1].drop("id"))))
            ), classes_metrics.iterrows())))

        method_keys = impl_smells_list + methods_metrics_dict.values()[0].keys()
        for method in set(methods_metrics_dict.keys() + smells_dict.keys()):
            d = dict(methods_metrics_dict.get(method, {}))
            d.update(smells_dict.get(method, {s: False for s in impl_smells_list}))
            self.designite[method] = d
        shutil.rmtree(out_dir)

    def _designite_helper(self, file_name, ids) -> pd.DataFrame:
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
        ck_jar = os.path.join(VersionMetrics.EXTERNALS, self.config['EXTERNALS']['CK'])
        command = ["java", "-jar", ck_jar, self.repo.local_path]
        Popen(command, cwd=out_dir).communicate()
        df = pd.read_csv(os.path.join(out_dir, "method.csv"))
        df = df.drop(['class', "method"], axis=1)
        df['method_id'] = df.apply(lambda x: self.get_closest_id(x['file'], x['line']), axis=1)
        df = df[list(map(lambda x: x is not None, df['method_id'].to_list()))]
        df = df.drop(['file', "line"], axis=1)
        df.apply(lambda x: self.ck.setdefault(x["method_id"], x.drop(("method_id"))), axis=1)
        shutil.rmtree(out_dir)

    def mood_data(self):
        self.mood = {}
        out_dir = tempfile.mkdtemp()
        mood_jar = os.path.join(VersionMetrics.EXTERNALS, self.config['EXTERNALS']['MOOD'])
        command = ["java", "-jar", mood_jar, self.repo.local_path, out_dir]
        Popen(command).communicate()
        with open(os.path.join(out_dir, "_metrics.json")) as f:
            self.mood = dict(map(lambda x: (self.classes_paths.get(x[0].lower()), x[1]), json.loads(f.read()).items()))
        shutil.rmtree(out_dir)

    def halstead_data(self):
        self.halstead = metrics_for_project(self.repo.local_path)


if __name__ == "__main__":
    main()
    # v = VersionMetrics("DL", r"C:\temp\DL", "0.3.51-RC1")
    # v.extract()
