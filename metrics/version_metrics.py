import os
import shutil
import tempfile
import json
from abc import ABC, abstractmethod
from subprocess import Popen
from xml.etree import ElementTree

import pandas as pd

from config import Config
from data_extractor import DataExtractor
from metrics.rsc import source_monitor_xml
from metrics.version_metrics_data import (
    Data,
    CompositeData, HalsteadData, CKData, SourceMonitorFilesData, SourceMonitorData, DesigniteDesignSmellsData,
    DesigniteImplementationSmellsData, DesigniteOrganicTypeSmellsData, DesigniteOrganicMethodSmellsData,
    DesigniteTypeMetricsData, DesigniteMethodMetricsData, CheckstyleData, BuggedData, BuggedMethodData)
from projects import Project
from repo import Repo
from .commented_code_detector import metrics_for_project
from metrics.rsc.designite_smells import (
    design_smells_list,
    implementation_smells_list,
    organic_type_smells_list,
    organic_method_smells_list)
from .java_analyser import JavaParserFileAnalyser


class Extractor(ABC):
    def __init__(self, extractor_name, project: Project, version, repo=None):
        self.extractor_name = extractor_name
        self.project = project
        self.project_name = project.github()
        self.version = version
        self.config = Config().config
        self.runner = self._get_runner(self.config, extractor_name)
        if repo is None:
            repo = Repo(project.jira(), project.github(), project.path(), version)
        self.local_path = os.path.realpath(repo.local_path)
        self.file_analyser = JavaParserFileAnalyser(self.local_path, self.project_name, self.version)
        self.data: Data = None

    @staticmethod
    def _get_runner(config, extractor_name):
        externals_path = config['EXTERNALS']['BaseDir']
        runner_name = config['EXTERNALS'][extractor_name]
        externals = Config.get_work_dir_path(externals_path)
        runner = os.path.join(externals, runner_name)
        return runner

    @abstractmethod
    def _extract(self):
        pass

    @abstractmethod
    def _set_data(self):
        pass

    def store(self):
        self.data.store()

    def extract(self):
        self._set_data()
        if hasattr(self.data, "path") and os.path.exists(self.data.path):
            return
        self._extract()
        self.store()


    @staticmethod
    def get_all_extractors(project, version, repo=None):
        for s in Extractor.__subclasses__():
            yield s(project, version, repo)


class Bugged(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Bugged", project, version, repo=repo)

    def _set_data(self):
        self.data = BuggedData(self.project, self.version)

    def _extract(self):
        extractor = DataExtractor(self.project)
        extractor.extract()
        path = extractor.get_bugged_files_path(self.version, True)
        df = pd.read_csv(path, sep=';')
        key = 'file_name'
        if 'method_id' in df.columns:
            key = 'method_id'
        bugged = df.groupby(key).apply(lambda x: dict(zip(["is_buggy"], x.is_buggy))).to_dict()
        self.data.set_raw_data(bugged)


class BuggedMethods(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("BuggedMethods", project, version, repo=repo)

    def _set_data(self):
        self.data = BuggedMethodData(self.project, self.version)

    def _extract(self):
        extractor = DataExtractor(self.project)
        extractor.extract(True)
        path = extractor.get_bugged_methods_path(self.version, True)
        df = pd.read_csv(path, sep=';')
        key = 'method_id'
        bugged = df.groupby(key).apply(lambda x: dict(zip(["is_method_buggy"], x.is_method_buggy))).to_dict()
        self.data.set_raw_data(bugged)


class Checkstyle(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Checkstyle", project, version, repo)
        self.out_path_to_xml = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['Checkstyle'])))

    def _set_data(self):
        self.data = CheckstyleData(self.project, self.version)

    def _extract(self):
        all_checks_xml = self._get_all_checks_xml(self.config)
        self._execute_command(self.runner, all_checks_xml, self.local_path, self.out_path_to_xml)
        checkstyle = self._process_checkstyle_data(self.out_path_to_xml)
        self.data.set_raw_data(checkstyle)

    @staticmethod
    def _get_all_checks_xml(config):
        externals_path = config['EXTERNALS']['BaseDir']
        all_checks_xml_name = config['EXTERNALS']['AllChecks']
        externals = Config.get_work_dir_path(externals_path)
        all_checks_xml = os.path.join(externals, all_checks_xml_name)
        return all_checks_xml

    @staticmethod
    def _execute_command(checkstyle_runner: str, all_checks_xml: str, local_path: str, out_path_to_xml: str) -> str:
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
        with open(out_path_to_xml) as file:
            root = ElementTree.parse(file).getroot()
            for file_element in root:
                try:
                    filepath = file_element.attrib['name']
                except:
                    continue
                if not filepath.endswith(".java"):
                    continue
                items, tmp, keys = self._get_items(file_element, os.path.realpath(filepath), tmp, keys)
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
                'file': file_path[len(os.path.realpath(self.local_path))+1:],
            })
            keys.add(key)
            method_id = self.file_analyser.get_closest_id(file_path, line)
            if method_id:
                tmp.setdefault(method_id, dict())[key] = value
        return file_element, tmp, keys


class Designite(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Designite", project, version, repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['Designite'])))

    def _set_data(self):
        self.data = CompositeData()

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_dir)
        design_code_smells = self._extract_design_code_smells()
        implementation_code_smells = self._extract_implementation_code_smells()
        organic_type_code_smells = self._extract_organic_type_code_smells()
        organic_method_code_smells = self._extract_organic_method_code_smells()
        type_metrics = self._extract_type_metrics()
        method_metrics = self._extract_method_metrics()
        self.data \
            .add(DesigniteDesignSmellsData(self.project, self.version, data=design_code_smells)) \
            .add(DesigniteImplementationSmellsData(self.project, self.version, data=implementation_code_smells)) \
            .add(DesigniteOrganicTypeSmellsData(self.project, self.version, data=organic_type_code_smells)) \
            .add(DesigniteOrganicMethodSmellsData(self.project, self.version, data=organic_method_code_smells)) \
            .add(DesigniteTypeMetricsData(self.project, self.version, data=type_metrics)) \
            .add(DesigniteMethodMetricsData(self.project, self.version, data=method_metrics))

    @staticmethod
    def _execute_command(designite_runner, local_path, out_dir):
        Config.assert_dir_exists(out_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        print(out_dir)
        commands = ["java", "-jar", designite_runner, "-i", local_path, "-o", out_dir]
        p = Popen(commands)
        p.communicate()
        return out_dir

    def _extract_design_code_smells(self):
        path = os.path.join(self.out_dir, r"designCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name"]
        smells_columns = design_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        design_smells = self._get_smells_dict(df, smells_columns)
        return design_smells

    def _extract_implementation_code_smells(self):
        path = os.path.join(self.out_dir, r"implementationCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "Method Name"]
        smells_columns = implementation_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        implementation_smells = self._get_smells_dict(df, smells_columns)
        return implementation_smells

    def _extract_organic_type_code_smells(self):
        path = os.path.join(self.out_dir, r"organicTypeCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name"]
        smells_columns = organic_type_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        organic_type_smells = self._get_smells_dict(df, smells_columns)
        return organic_type_smells

    def _extract_organic_method_code_smells(self):
        path = os.path.join(self.out_dir, r"organicMethodCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "Method Name"]
        smells_columns = organic_method_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        organic_method_smells = self._get_smells_dict(df, smells_columns)
        return organic_method_smells

    def _extract_type_metrics(self):
        path = os.path.join(self.out_dir, r"typeMetrics.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name"]
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns, self.local_path)
        type_metrics = self._get_metrics_dict(df)
        return type_metrics

    def _extract_method_metrics(self):
        path = os.path.join(self.out_dir, r"methodMetrics.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "MethodName"]
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
    def __init__(self, project: Project, version, repo=None):
        super().__init__("SourceMonitor", project, version, repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['SourceMonitor'])))


    def _set_data(self):
        self.data = CompositeData()

    def _extract(self):
        if os.name == "nt":
            self._execute_command(self.runner, self.local_path, self.out_dir)
            source_monitor_files, source_monitor = self._process_metrics()
            self.data \
                .add(SourceMonitorFilesData(self.project, self.version, data=source_monitor_files)) \
                .add(SourceMonitorData(self.project, self.version, data=source_monitor))

    @staticmethod
    def _execute_command(source_monitor_runner, local_path, out_dir):
        xml = source_monitor_xml.xml \
            .replace("verP", out_dir) \
            .replace("verREPO", local_path)
        xml_path = os.path.join(out_dir, "sourceMonitor.xml")
        with open(xml_path, "w") as f:
            f.write(xml)

        Popen([source_monitor_runner, "/C", xml_path]).communicate()
        return out_dir

    def _process_metrics(self):
        files_path = os.path.join(self.out_dir, "source_monitor_classes.csv")
        files_df = pd.read_csv(files_path, encoding = "ISO-8859-8", error_bad_lines=False)
        files_df["Maximum Block Depth"] = files_df["Maximum Block Depth"].apply(lambda x: float(str(x).replace('+', '')))
        cols_to_drop = ["Project Name", "Checkpoint Name", "Created On"]
        for i in cols_to_drop + ['Name of Most Complex Method*']:
            files_df = files_df.drop(i, axis=1)
        files_cols = list(files_df.rename(columns={"Statements":"FileStatements"}).columns.drop("File Name"))
        source_monitor_files = dict(
            map(lambda x: (
                x[1]["File Name"],
                dict(zip(files_cols, list(x[1].drop("File Name"))))
            ), files_df.iterrows()))

        methods_path = os.path.join(self.out_dir, "source_monitor_methods.csv")
        methods_df = pd.read_csv(methods_path, encoding = "ISO-8859-8", error_bad_lines=False)
        for i in cols_to_drop:
            methods_df = methods_df.drop(i, axis=1)
        methods_cols = list(methods_df.columns.drop("File Name").drop("Method"))
        source_monitor = dict(map(lambda x: (
            self._get_source_monitor_id(
                x[1]["File Name"],
                x[1]["Method"],
                self.file_analyser.methods_by_path_and_name),
            dict(zip(
                methods_cols,
                list(x[1].drop("File Name").drop("Method"))))),
                                  methods_df.iterrows()))
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
    def __init__(self, project: Project, version, repo=None):
        super().__init__("CK", project, version, repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['CK'])))

    def _set_data(self):
        self.data = CKData(self.project, self.version)

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_dir)
        ck = self._process_metrics()
        self.data.set_raw_data(ck)

    @staticmethod
    def _execute_command(ck_runner, local_path, out_dir):
        project_path = os.path.join(os.getcwd(), local_path)
        command = ["java", "-jar", ck_runner, project_path, "True"]
        Popen(command, cwd=out_dir).communicate()
        return out_dir

    def _process_metrics(self):
        ck = {}
        df_path = os.path.join(self.out_dir, "method.csv")
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
        return ck


# class Mood(Extractor):
#     def __init__(self, project: Project, version, repo=None):
#         super().__init__("MOOD", project, version, repo)
#
#     def _set_data(self):
#         from metrics.version_metrics_data import MoodData
#         self.data = MoodData(self.project, self.version)
#
#     def _extract(self):
#         out_dir = self._execute_command(self.runner, self.local_path)
#         mood = self._process_metrics(out_dir)
#         self.data.set_raw_data(mood)
#
#     @staticmethod
#     def _execute_command(mood_runner, local_path):
#         out_dir = tempfile.mkdtemp()
#         command = ["java", "-jar", mood_runner, local_path, out_dir]
#         Popen(command).communicate()
#         return out_dir
#
#     # TODO There is a but with the Mood id
#     def _process_metrics(self, out_dir):
#         with open(os.path.join(out_dir, "_metrics.json")) as file:
#             mood = dict(map(lambda x: (
#                 self.file_analyser.classes_paths.get(x[0].lower()),
#                 x[1]),
#                             json.loads(file.read()).items()))
#         shutil.rmtree(out_dir)
#         return mood


class Halstead(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Halstead", project, version, repo)

    def _set_data(self):
        self.data = HalsteadData(self.project, self.version)

    def _extract(self):
        halstead = metrics_for_project(self.local_path)
        self.data.set_raw_data(halstead)
