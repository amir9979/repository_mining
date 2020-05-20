import os
import shutil
import tempfile
import json
from abc import ABC, abstractmethod
from subprocess import Popen
from xml.etree import ElementTree

import pandas as pd

from caching import cached
from config import Config
from javadiff.javadiff.SourceFile import SourceFile
from metrics.rsc import source_monitor_xml
from metrics.version_metrics_data import (
    Data,
    CompositeData, HalsteadData, MoodData, CKData, SourceMonitorFilesData, SourceMonitorData, DesigniteDesignSmellsData,
    DesigniteImplementationSmellsData, DesigniteOrganicTypeSmellsData, DesigniteOrganicMethodSmellsData,
    DesigniteTypeMetricsData, DesigniteMethodMetricsData, CheckstyleData)
from repo import Repo
from .commented_code_detector import metrics_for_project
from metrics.rsc.designite_smells import (
    design_smells_list,
    implementation_smells_list,
    organic_type_smells_list,
    organic_method_smells_list)


class FileAnalyser:
    def __init__(self, local_path, project_name, version_name):
        self.local_path = local_path
        cache_name = self._get_cache_name(project_name, version_name)
        analyze = cached(cache_name)(self._analyze)
        res = analyze(local_path)
        self.methods = res[0]
        self.methods_df = self._store_methods(project_name, version_name, self.methods)
        self.methods_by_file_line = res[1]
        self.classes_paths = res[2]
        self.methods_by_name = res[3]
        self.methods_by_path_and_name = res[4]

    def get_closest_id(self, file_name, line):
        method_id = None
        for line_ in [line, line + 1, line - 1]:
            file_path = (file_name.split(self.local_path)[1][1:], line_)
            if file_path in self.methods_by_file_line:
                method_id = self.methods_by_file_line[file_path]
                break
        return method_id

    def get_methods_from_file(self, file):
        cond = self.methods_df['file_name'] == file
        return self.methods_df.loc[cond].method_name

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
            for name in filter(lambda y: "Test" not in y, filter(lambda x: x.endswith(".java"), files)):
                with open(os.path.join(root, name), encoding='latin-1') as f:
                    contents = f.read()
                    file_name = os.path.join(root, name)[len(local_path) + 1:]
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
        if os.path.exists(out_path):
            return pd.read_csv(out_path)
        columns = ["method_id", "file_name", "method_name", "start_line", "end_line"]
        values = list(map(lambda m: [m.id, m.file_name, m.method_name, m.start_line, m.end_line], methods))
        df = pd.DataFrame(values, columns=columns)
        df.to_csv(out_path, index=False)
        return df

    @staticmethod
    def _extract_classes(sf, classes_paths):
        for m in sf.modified_names:
            classes_paths[m.lower()] = sf.file_name

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
    def __init__(self, extractor_name, github_project_name, version, jira_project_name, local_path):
        self.extractor_name = extractor_name
        self.project = github_project_name
        self.version = version
        self.config = Config().config
        self.runner = self._get_runner(self.config, extractor_name)
        repo = Repo(jira_project_name, github_project_name, local_path, version)
        self.local_path = repo.local_path
        self.file_analyser = FileAnalyser(self.local_path, self.project, self.version)
        self.data: Data = None

    @staticmethod
    def _get_runner(config, extractor_name):
        externals_path = config['EXTERNALS']['BaseDir']
        runner_name = config['EXTERNALS'][extractor_name]
        externals = Config.get_work_dir_path(externals_path)
        runner = os.path.join(externals, runner_name)
        return runner

    @abstractmethod
    def extract(self, jira_project_name, github_name, local_path):
        pass


class Bugged(Extractor):

    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(Bugged, self).__init__("Bugged", github_project_name, version, jira_project_name, local_path)

    def extract(self, jira_project_name, github_name, local_path):

        self._process_bugged_data(path)
        pass


class Checkstyle(Extractor):
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(Checkstyle, self).__init__("Checkstyle", github_project_name, version, jira_project_name, local_path)

    def extract(self):
        all_checks_xml = self._get_all_checks_xml(self.config)
        out_path_to_xml = self._execute_command(self.runner, all_checks_xml, self.local_path)
        checkstyle = self._process_checkstyle_data(out_path_to_xml)
        self.data = CheckstyleData(self.project, self.version, data=checkstyle)
        self.data.store()

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

    def _process_checkstyle_data(self, out_path_to_xml):
        files = {}
        tmp = {}
        keys = set()
        with(open(out_path_to_xml)) as file:
            for file_element in ElementTree.parse(file).getroot():
                filepath = file_element.attrib['name']
                items, tmp, keys = self._get_items(file_element, filepath, tmp, keys)
                files[filepath] = items
        checkstyle = {}
        for method_id in tmp:
            checkstyle[method_id] = dict.fromkeys(keys, 0)
            checkstyle[method_id].update(tmp[method_id])
        return checkstyle

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
            method_id = self.file_analyser.get_closest_id(file_path, line)
            if method_id:
                tmp.setdefault(method_id, dict())[key] = value
        return file_element, tmp, keys


class Designite(Extractor):
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super().__init__("Designite", github_project_name, version, jira_project_name, local_path)

    def extract(self):
        out_dir = self._execute_command(self.runner, self.local_path)
        design_code_smells = self._extract_design_code_smells(out_dir)
        implementation_code_smells = self._extract_implementation_code_smells(out_dir)
        organic_type_code_smells = self._extract_organic_type_code_smells(out_dir)
        organic_method_code_smells = self._extract_organic_method_code_smells(out_dir)
        type_metrics = self._extract_type_metrics(out_dir)
        method_metrics = self._extract_method_metrics(out_dir)

        self.data = CompositeData()
        self.data \
            .add(DesigniteDesignSmellsData(self.project, self.version, data=design_code_smells)) \
            .add(DesigniteImplementationSmellsData(self.project, self.version, data=implementation_code_smells)) \
            .add(DesigniteOrganicTypeSmellsData(self.project, self.version, data=organic_type_code_smells)) \
            .add(DesigniteOrganicMethodSmellsData(self.project, self.version, data=organic_method_code_smells)) \
            .add(DesigniteTypeMetricsData(self.project, self.version, data=type_metrics)) \
            .add(DesigniteMethodMetricsData(self.project, self.version, data=method_metrics)) \
            .store()

    @staticmethod
    def _execute_command(designite_runner, local_path):
        out_dir = tempfile.mkdtemp()
        commands = ["java",
                    "-jar", designite_runner,
                    "-i", local_path,
                    "-o", out_dir]
        Popen(commands).communicate()
        return out_dir

    def _extract_design_code_smells(self, out_dir):
        path = os.path.join(out_dir, r"designCodeSmells.csv")
        keys_columns = ["File Path", "Package Name", "Type Name"]
        smells_columns = design_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        design_smells = self._get_smells_dict(df, smells_columns)
        return design_smells

    def _extract_implementation_code_smells(self, out_dir):
        path = os.path.join(out_dir, r"implementationCodeSmells.csv")
        keys_columns = ["File Path", "Package Name", "Type Name", "Method Name"]
        smells_columns = implementation_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        implementation_smells = self._get_smells_dict(df, smells_columns)
        return implementation_smells

    def _extract_organic_type_code_smells(self, out_dir):
        path = os.path.join(out_dir, r"organicTypeCodeSmells.csv")
        keys_columns = ["File Path", "Package Name", "Type Name"]
        smells_columns = organic_type_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        organic_type_smells = self._get_smells_dict(df, smells_columns)
        return organic_type_smells

    def _extract_organic_method_code_smells(self, out_dir):
        path = os.path.join(out_dir, r"organicMethodCodeSmells.csv")
        keys_columns = ["File Path", "Package Name", "Type Name", "Method Name"]
        smells_columns = organic_method_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        organic_method_smells = self._get_smells_dict(df, smells_columns)
        return organic_method_smells

    def _extract_type_metrics(self, out_dir):
        path = os.path.join(out_dir, r"typeMetrics.csv")
        keys_columns = ["File Path", "Package Name", "Type Name"]
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        type_metrics = self._get_metrics_dict(df)
        return type_metrics

    def _extract_method_metrics(self, out_dir):
        path = os.path.join(out_dir, r"methodMetrics.csv")
        keys_columns = ["File Path", "Package Name", "Type Name", "MethodName"]
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        type_metrics = self._get_metrics_dict(df)
        return type_metrics

    @staticmethod
    def _process_keys(df, keys_columns, local_path):
        df = df.drop(r"Project Name", axis=1)
        df = df.dropna()
        df["id"] = df.apply(
            lambda x: ".".join(map(lambda y: x[y], keys_columns)), axis=1)
        df["id"] = df["id"].apply(lambda x: x.replace('.java.', '.java@', 1))
        base_dir = os.path.join(os.getcwd(), local_path, '')
        df["id"] = df["id"].apply(lambda x: x.replace(base_dir, ''))
        for i in keys_columns:
            df = df.drop(i, axis=1)
        return df

    @staticmethod
    def _get_smells_dict(df, smells_columns) -> dict:
        smells_for_id = {}
        for id_ in df["id"]:
            smells_for_id[id_] = dict.fromkeys(smells_columns, False)
        for line, data in df.iterrows():
            smells_for_id[data["id"]][data["Code Smell"]] = True
        return smells_for_id

    @staticmethod
    def _get_metrics_dict(df) -> dict:
        types = {}
        metrics_columns = list(df.columns.drop("id"))
        for id_ in df["id"]:
            types[id_] = dict.fromkeys(metrics_columns, False)
        types.update(
            dict(map(lambda x: (
                x[1]["id"],
                dict(zip(metrics_columns, list(x[1].drop("id"))))
            ), df.iterrows())))
        return types


class SourceMonitor(Extractor):
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(SourceMonitor, self).__init__("SourceMonitor", github_project_name, version, jira_project_name,
                                            local_path)

    def extract(self):
        if not os.name == "dt":
            # TODO Create an EmptyData class
            return

        out_dir = self._execute_command(self.runner, self.local_path)
        source_monitor_files, source_monitor = self._process_metrics(out_dir)
        self.data = CompositeData()
        self.data \
            .add(SourceMonitorFilesData(self.project, self.version, data=source_monitor_files)) \
            .add(SourceMonitorData(self.project, self.version, data=source_monitor)) \
            .store()

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
                self.file_analyser.methods_by_path_and_name),
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
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(CK, self).__init__("CK", github_project_name, version, jira_project_name, local_path)

    def extract(self):
        out_dir = self._execute_command(self.runner, self.local_path)
        ck = self._process_metrics(out_dir)
        self.data = CKData(self.project, self.version, data=ck)
        self.data.store()

    @staticmethod
    def _execute_command(ck_runner, local_path):
        out_dir = tempfile.mkdtemp()
        project_path = os.path.join(os.getcwd(), local_path)
        command = ["java", "-jar", ck_runner, project_path, "True"]
        Popen(command, cwd=out_dir).communicate()
        return out_dir

    def _process_metrics(self, out_dir):
        ck = {}

        df_path = os.path.join(out_dir, "method.csv")
        df = pd.read_csv(df_path)
        df = df.drop(['class', "method"], axis=1)
        df['method_id'] = df.apply(lambda x:
                                   self.file_analyser.get_closest_id(x['file'], x['line']),
                                   axis=1)
        df = df[list(map(lambda x: x is not None, df['method_id'].to_list()))]
        df = df.drop(['file', "line"], axis=1)
        df.apply(lambda x:
                 ck.setdefault(x["method_id"], x.drop("method_id")),
                 axis=1)

        shutil.rmtree(out_dir)
        return ck


class Mood(Extractor):
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(Mood, self).__init__("MOOD", github_project_name, version, jira_project_name, local_path)

    def extract(self):
        out_dir = self._execute_command(self.runner, self.local_path)
        mood = self._process_metrics(out_dir)
        self.data = MoodData(self.project, self.version, data=mood)
        self.data.store()

    @staticmethod
    def _execute_command(mood_runner, local_path):
        out_dir = tempfile.mkdtemp()
        command = ["java", "-jar", mood_runner, local_path, out_dir]
        Popen(command).communicate()
        return out_dir

    # TODO There is a but with the Mood id
    def _process_metrics(self, out_dir):
        with open(os.path.join(out_dir, "_metrics.json")) as file:
            mood = dict(map(lambda x: (
                self.file_analyser.classes_paths.get(x[0].lower()),
                x[1]),
                            json.loads(file.read()).items()))
        shutil.rmtree(out_dir)
        return mood


class Halstead(Extractor):
    def __init__(self, github_project_name, version, jira_project_name, local_path):
        super(Halstead, self).__init__("Halstead", github_project_name, version, jira_project_name, local_path)

    def extract(self):
        halstead = metrics_for_project(self.local_path)
        self.data = HalsteadData(self.project, self.version, data=halstead)
        self.data.store()
