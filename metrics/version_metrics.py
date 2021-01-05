import os
import json
from abc import ABC, abstractmethod
from subprocess import Popen
from xml.etree import ElementTree
from datetime import datetime
import pandas as pd
import math
import git
from functools import reduce
from collections import Counter

from config import Config
from data_extractor import DataExtractor
from metrics.rsc import source_monitor_xml
from metrics.version_metrics_data import (
    Data,
    CompositeData, HalsteadData, CKData, SourceMonitorFilesData, SourceMonitorData, DesigniteDesignSmellsData,
    DesigniteImplementationSmellsData, DesigniteOrganicTypeSmellsData, DesigniteOrganicMethodSmellsData,
    DesigniteTypeMetricsData, DesigniteMethodMetricsData, CheckstyleData, BuggedData, BuggedMethodData, MoodData,
    JasomeFilesData, JasomeMethodsData, ProcessData, IssuesData, JasomeMoodData, JasomeCKData, JasomeLKData)
from projects import Project
from repo import Repo
from .commented_code_detector import metrics_for_project, Halstead, CommentFilter
from metrics.rsc.designite_smells import (
    design_smells_list,
    implementation_smells_list,
    organic_type_smells_list,
    organic_method_smells_list)
from .java_analyser import JavaParserFileAnalyser
from metrics.version_metrics_name import DataType
from typing import List


class Extractor(ABC):
    def __init__(self, extractor_name, project: Project, version, data_types: List[DataType], repo=None):
        self.extractor_name = extractor_name
        self.project = project
        self.project_name = project.github_name
        self.version = version
        self.data_types = data_types
        self.config = Config().config
        self.runner = self._get_runner(self.config, extractor_name)
        if repo is None:
            repo = Repo(project, version)
        self.local_path = os.path.realpath(repo.project.path)
        self.file_analyser = JavaParserFileAnalyser(self.local_path, self.project_name, self.version)
        self.data: Data = None

    @staticmethod
    def _get_runner(config, extractor_name):
        if extractor_name not in config['EXTERNALS']:
            return ''
        externals_path = config['EXTERNALS']['BaseDir']
        runner_name = config['EXTERNALS'][extractor_name]
        externals = Config.get_work_dir_path(externals_path)
        runner = os.path.join(externals, runner_name)
        return runner

    @abstractmethod
    def _extract(self):
        pass

    # @abstractmethod
    def _execute(self):
        pass

    # @abstractmethod
    def _process_data(self):
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
        super().__init__("Bugged", project, version, [DataType.BuggedDataType], repo=repo)

    def _set_data(self):
        self.data = BuggedData(self.project, self.version)

    def _extract(self):
        extractor = DataExtractor(self.project)
        path = extractor.get_bugged_files_path(self.version, True)
        df = pd.read_csv(path, sep=';')
        key = 'file_name'
        assert key in df.columns
        bugged = df.groupby(key).apply(lambda x: dict(zip(["is_buggy"], x.is_buggy))).to_dict()
        self.data.set_raw_data(bugged)


class BuggedMethods(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("BuggedMethods", project, version, [DataType.BuggedMethodsDataType], repo=repo)

    def _set_data(self):
        self.data = BuggedMethodData(self.project, self.version)

    def _extract(self):
        extractor = DataExtractor(self.project)
        path = extractor.get_bugged_methods_path(self.version)
        df = pd.read_csv(path, sep=';')
        key = 'method_id'
        bugged = df.groupby(key).apply(lambda x: dict(zip(["is_method_buggy"], x.is_method_buggy))).to_dict()
        self.data.set_raw_data(bugged)


class Checkstyle(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Checkstyle", project, version, [DataType.CheckstyleDataType], repo)
        self.out_path_to_xml = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['Checkstyle'])))

    def _set_data(self):
        self.data = CheckstyleData(self.project, self.version)

    def _extract(self):
        all_checks_xml = self._get_all_checks_xml(self.config)
        self._execute_command(self.runner, all_checks_xml, self.local_path, self.out_path_to_xml.replace("\\\\?\\", ""))
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
                    "-o", out_path_to_xml.replace("\\\\?\\", ""),
                    local_path]
        p = Popen(commands)
        p.communicate()
        return out_path_to_xml

    def _process_checkstyle_data(self, out_path_to_xml):
        files = {}
        tmp = {}
        keys = set()
        with open(out_path_to_xml, "r", encoding="utf-8") as file:
            root = ElementTree.parse(file).getroot()
            for file_element in root:
                try:
                    filepath = file_element.attrib['name'].lower()
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
                if "npath" in key.lower():
                    value = min(10000, int(value))
                tmp.setdefault(method_id, dict())[key] = value
        return file_element, tmp, keys


class Designite(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Designite", project, version, [DataType.DesigniteDesignSmellsDataType, DataType.DesigniteImplementationSmellsDataType,
                                                         DataType.DesigniteMethodMetricsDataType, DataType.DesigniteOrganicMethodSmellsDataType,
                                                         DataType.DesigniteTypeMetricsDataType, DataType.DesigniteOrganicTypeSmellsDataType], repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['Designite'])))
        Config.assert_dir_exists(self.out_dir)

    def _set_data(self):
        self.data = CompositeData()

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_dir.replace("\\\\?\\", ""))
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
        df = self._process_keys(df, keys_columns)
        design_smells = self._get_smells_dict(df, smells_columns)
        return design_smells

    def _extract_implementation_code_smells(self):
        path = os.path.join(self.out_dir, r"implementationCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "Method Name"]
        smells_columns = implementation_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns)
        implementation_smells = self._get_smells_dict(df, smells_columns)
        return implementation_smells

    def _extract_organic_type_code_smells(self):
        path = os.path.join(self.out_dir, r"organicTypeCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name"]
        smells_columns = organic_type_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns)
        organic_type_smells = self._get_smells_dict(df, smells_columns)
        return organic_type_smells

    def _extract_organic_method_code_smells(self):
        path = os.path.join(self.out_dir, r"organicMethodCodeSmells.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "Method Name"]
        smells_columns = organic_method_smells_list
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns)
        organic_method_smells = self._get_smells_dict(df, smells_columns)
        return organic_method_smells

    def _extract_type_metrics(self):
        path = os.path.join(self.out_dir, r"typeMetrics.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name"]
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns)
        type_metrics = self._get_metrics_dict(df)
        return type_metrics

    def _extract_method_metrics(self):
        path = os.path.join(self.out_dir, r"methodMetrics.csv")
        if not os.path.exists(path):
            return {}
        keys_columns = ["Package Name", "Type Name", "MethodName"]
        df = pd.read_csv(path)
        df = self._process_keys(df, keys_columns)
        type_metrics = self._get_metrics_dict(df)
        return type_metrics

    def _process_keys(self,df, keys_columns):
        df = df.drop(r"Project Name", axis=1)
        df = df.dropna()
        df["id"] = df.apply(lambda x: self.file_analyser.get_file_path_by_designite(*list(map(lambda y: x[y], keys_columns))), axis=1)
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
        super().__init__("SourceMonitor", project, version, [DataType.SourceMonitorDataType, DataType.SourceMonitorFilesDataType], repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['SourceMonitor'])))
        Config.assert_dir_exists(self.out_dir)


    def _set_data(self):
        self.data = CompositeData()

    def _extract(self):
        if os.name == "nt":
            self._execute_command(self.runner, self.local_path, self.out_dir.replace("\\\\?\\", ""))
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
        files_df['full_id'] = files_df.apply(lambda x: x['File Name'], axis=1)
        files_df = files_df.dropna()
        files_df = files_df.drop(['File Name'], axis=1)
        source_monitor_files = dict(
            map(lambda x: (
                x[1]['full_id'],
                dict(zip(files_cols, list(x[1].drop('full_id'))))
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
        super().__init__("CK", project, version, [DataType.CKDataType], repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['CK'])))
        Config.assert_dir_exists(self.out_dir)

    def _set_data(self):
        self.data = CKData(self.project, self.version)

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_dir.replace("\\\\?\\", ""))
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


class Mood(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("MOOD", project, version, [DataType.MoodDataType], repo)
        self.out_dir = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['MOOD'])))
        Config.assert_dir_exists(self.out_dir)


    def _set_data(self):
        self.data = MoodData(self.project, self.version)

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_dir)
        mood = self._process_metrics()
        self.data.set_raw_data(mood)

    @staticmethod
    def _execute_command(mood_runner, local_path, out_dir):
        command = ["java", "-jar", mood_runner, local_path, out_dir]
        Popen(command).communicate()

    def _process_metrics(self):
        with open(os.path.join(self.out_dir, "_metrics.json")) as file:
            mood = dict(map(lambda x: (
                self.file_analyser.classes_paths.get(x[0].lower()),
                x[1]), json.loads(file.read()).items()))
        return mood


class Halstead(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Halstead", project, version, [DataType.HalsteadDataType], repo)

    def _set_data(self):
        self.data = HalsteadData(self.project, self.version)

    def _extract(self):
        self.data.set_raw_data(metrics_for_project(self.local_path))


class Jasome(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("Jasome", project, version, [DataType.JasomeFilesDataType,DataType.JasomeCKDataType,
                                                      DataType.JasomeLKDataType,DataType.JasomeMoodDataType,
                                                      DataType.JasomeMethodsDataType], repo)
        self.out_path_to_xml = os.path.normpath(Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['TEMP']['Jasome'])))

    def _set_data(self):
        self.data = CompositeData()

    def _extract(self):
        self._execute_command(self.runner, self.local_path, self.out_path_to_xml)
        classes_metrics, methods_metrics = self._process_metrics()
        self.data \
            .add(JasomeFilesData(self.project, self.version, data=classes_metrics)) \
            .add(JasomeCKData(self.project, self.version, data=classes_metrics)) \
            .add(JasomeLKData(self.project, self.version, data=classes_metrics)) \
            .add(JasomeMoodData(self.project, self.version, data=classes_metrics)) \
            .add(JasomeMethodsData(self.project, self.version, data=methods_metrics))

    @staticmethod
    def _execute_command(jasome_runner, local_path, out_path_to_xml):
        command = ["java", "-cp", jasome_runner, "org.jasome.executive.CommandLineExecutive", '-xt', local_path, '-o', out_path_to_xml]
        print('jasome command', command)
        Popen(command).communicate()

    def _process_metrics(self):
        from metrics.jasome_xml_parser import parse
        classes_metrics, methods_metrics = parse(self.out_path_to_xml)
        classes_metrics["id"] = classes_metrics.apply(lambda x: self.file_analyser.classes_paths.get(x['Class Path'].lower()), axis=1)
        classes_metrics = classes_metrics.drop('Class Path', axis=1)
        cols = classes_metrics.columns.tolist()
        cols.remove("id")
        classes_metrics = classes_metrics[["id"] + cols]

        methods_metrics["id"] = methods_metrics.apply(lambda x: self.file_analyser.get_closest_id(x['File Name'], x['start_line']), axis=1)
        methods_metrics = methods_metrics.drop('File Name', axis=1)
        methods_metrics = methods_metrics.drop('start_line', axis=1)
        cols = methods_metrics.columns.tolist()
        cols.remove("id")
        methods_metrics = methods_metrics[["id"] + cols]
        return self._get_metrics_dict(classes_metrics), self._get_metrics_dict(methods_metrics)

    @staticmethod
    def _get_metrics_dict(df):
        types = {}
        metrics_columns = list(df.columns.drop("id"))
        for id_ in df["id"]:
            types[id_] = dict.fromkeys(metrics_columns, 0)
        types.update(
            dict(map(lambda x: (
                x[1]["id"],
                dict(zip(metrics_columns, list(x[1].drop("id"))))
            ), df.iterrows())))
        return types


class ProcessExtractor(Extractor):
    def __init__(self, project: Project, version, repo=None):
        super().__init__("ProcessExtractor", project, version, [DataType.ProcessFilesDataType, DataType.IssuesFilesDataType], repo)

    def _set_data(self):
        self.data = CompositeData()

    def clean(self, s):
        return "".join(list(filter(lambda c: c.isalpha(), s)))

    def _extract(self):
        # get version_date from apache_versions
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        path = os.path.join(repository_data, config['DATA_EXTRACTION']["AllVersions"], self.project.github_name, self.project.github_name + ".csv")
        df = pd.read_csv(path, sep=';')
        version_date = df[df['version_name'] == self.version]['version_date'].to_list()[0]
        version_date = datetime.strptime(version_date, '%Y-%m-%d %H:%M:%S')
        # get file list from committed_files
        path = os.path.join(repository_data, config['DATA_EXTRACTION']["CommittedFiles"], self.project.github_name, self.project.github_name + ".csv")
        df = pd.read_csv(path, sep=';')
        issues_path = os.path.join(repository_data, config['DATA_EXTRACTION']["Issues"], self.project.github_name,
                                   self.project.github_name + "_dummies.csv")
        issues_df = pd.read_csv(issues_path, sep=';')
        issues_df = df[['commit_id', 'issue_id']].merge(issues_df, on=['issue_id'], how='right')
        # filter commits after version date
        df = df[df.apply(lambda r: datetime.strptime(r['commit_date'], '%Y-%m-%d %H:%M:%S') < version_date, axis=1)]
        # split by file_name
        data = {}
        issues_data = {}

        extractor = DataExtractor(self.project)
        path = extractor.get_bugged_files_path(self.version, True)
        files = pd.read_csv(path, sep=';')['file_name'].to_list()
        df = df[df.apply(lambda r: r['file_name'].endswith('.java') and r['file_name'] in files, axis=1)]

        for file_name, file_df in df.groupby('file_name', as_index=False):
            data[file_name] = self._extract_process_features(file_df)
            issues_data[file_name] = self._extract_issues_features(file_df, issues_df, self._get_blame_data(file_name))
        # extract the following features:
        self.data.add(ProcessData(self.project, self.version, data=data)).add(IssuesData(self.project, self.version, data=issues_data))

    def _get_blame_data(self, file_name):
        repo = git.Repo(self.local_path)
        version_names = list(map(lambda x: x.name, repo.tags))
        version = self.version
        if version not in version_names:
            if '\\' in version:
                if version.replace('\\', '/') in version_names:
                    version = version.replace('\\', '/')
            if '/' in version:
                if version.replace('/', '\\') in version_names:
                    version = version.replace('/', '\\')
        blame = repo.blame(version, file_name)
        blame = reduce(list.__add__, map(lambda x: list(map(lambda y: (x[0], y), x[1])), blame), [])
        commits, source_code = list(zip(*blame))
        lines = CommentFilter().filterComments(source_code)[0]
        values = []
        for c, l in zip(commits, lines):
            d = {"commit_id": c.hexsha}
            for k, v in l.getValuesVector().items():
                d['blame_' + k.replace('Halstead', 'get')] = v
            values.append(d)
        return pd.DataFrame(values)

    def _get_blame_for_file(self, file_name):
        ans = {}
        repo = git.Repo(self.local_path)
        blame = repo.blame(self.version, file_name)
        ans['blobs'] = len(blame)
        blame = reduce(list.__add__, map(lambda x: list(map(lambda y: (x[0], y), x[1])), blame), [])
        commits, source_code = list(zip(*blame))
        ans['blame_commits'] = len(set(commits))
        c = dict(Counter(list(map(lambda x: x.hexsha, commits))))
        list(map(lambda x: c.update({x: c[x] / ans['blame_commits']}), c.keys()))
        for k, v in pd.DataFrame(c.values(), columns=['col']).describe().to_dict()['col'].items():
            ans['blame_' + k] = v

        lines = CommentFilter().filterComments(source_code)[0]
        commits_lines = list(filter(lambda x: x[1], zip(commits, lines)))
        filtered_commits, _ = set(zip(*commits_lines))
        c = dict(Counter(list(map(lambda x: x.hexsha, filtered_commits))))
        ans['blame_filtered_commits'] = len(set(zip(*commits_lines)))
        list(map(lambda x: c.update({x: c[x] / ans['blame_filtered_commits']}), c.keys()))
        for k, v in pd.DataFrame(c.values(), columns=['col']).describe().to_dict()['col'].items():
            ans['blame_filtered_' + k] = v
        values = []
        for c in set(filtered_commits):
            l = list(map(lambda l: l[1], filter(lambda l: l[0] == c, commits_lines)))
            h = Halstead(l).getValuesVector()
            values.append(h)
        for col, d in pd.DataFrame(values).describe().to_dict().items():
            for k, v in d.items():
                ans['blame_halstead_' + col + "_" + k] = v
        return ans

    def _get_features(self, d, initial=''):
        ans = {initial + "_count": d.shape[0]}
        des = d.describe()
        des = des.drop(['25%', '50%', '75%'])
        for col in des:
            for metric in des.index.to_list():
                # set default value
                ans["_".join([initial, col, metric])] = 0.0
        for col in des:
            for k, v in des[col].to_dict().items():
                if v and not math.isnan(v):
                    ans["_".join([self.clean(initial), self.clean(col), self.clean(k)])] = v
        return ans

    def _extract_process_features(self, df):
        df = df.drop(['file_name', 'is_java', 'commit_id', 'commit_date', 'commit_url', 'bug_url'], axis=1)
        ans = {}
        ans.update(self._get_features(df.drop('issue_id', axis=1), "all_process"))
        return ans

    def _extract_issues_features(self, df, issues_df, blame):
        ans = {}
        # d = df[['commit_id', 'issue_id']]
        # blame_merge = d.merge(blame, on=['commit_id'], how='right')
        blame_merge = blame.merge(issues_df, on=['commit_id'], how='left')
        blame_merge = blame_merge.drop(['commit_id', 'issue_id'], axis=1)
        ans.update(self._get_features(blame_merge, "blame_merge"))
        df = df.drop(['file_name', 'is_java', 'commit_id', 'commit_date', 'commit_url', 'bug_url'], axis=1)
        ans.update(self._get_features(df[df['issue_id'] != '0'].drop('issue_id', axis=1), "fixes"))
        ans.update(self._get_features(df[df['issue_id'] == '0'].drop('issue_id', axis=1), "non_fixes"))
        merged = df.merge(issues_df.drop(['commit_id'], axis=1), on=['issue_id'], how='inner')
        merged = merged.drop(['issue_id'], axis=1)
        ans.update(self._get_features(merged, 'issues'))

        # for dummy in dummies_dict:
        #     # percent
        #     for d in dummies_dict[dummy]:
        #         ans.update(self._get_features(merged[merged[d] == 1].drop(d, axis=1), d))
        #         ans.update(self._get_features(blame_merge[blame_merge[d] == 1], d))

        return ans