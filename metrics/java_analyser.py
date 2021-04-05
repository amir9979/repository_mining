import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from subprocess import Popen, run

import pandas as pd

from caching import cached
from config import Config
try:
    from javadiff.javadiff.SourceFile import SourceFile
except:
    from javadiff.SourceFile import SourceFile

import psutil
from threading import Timer
from subprocess import run, Popen, TimeoutExpired

TIMEOUT = 5 * 60


def kill_proc(proc):
    proc.kill()
    proc.terminate()
    psutil.Process(proc.pid)


def execute_timeout(commands, cwd=None):
    print(commands)
    with Popen(commands, cwd=cwd) as proc:
        try:
            timer = Timer(TIMEOUT, lambda : kill_proc(proc))
            timer.start()
            proc.communicate(timeout=TIMEOUT)
            timer.cancel()
        except TimeoutExpired:
            try:
                kill_proc(proc)
                timer.cancel()
            except:
                pass
        except:
            pass



class FileAnalyser(ABC):
    @abstractmethod
    def get_closest_id(self, file_name, line):
        pass


class JavaParserFileAnalyser(FileAnalyser):

    def __init__(self, local_path, project_name, version_name):
        self.local_path = local_path
        self.project_name = project_name
        self.version_name = version_name
        self.outpath = self._get_outpath(project_name, version_name)
        parser_df = self._get_cached(self.outpath)
        if parser_df is None:
            parser_df = self._parse_source_code(local_path, self.outpath)
        self.parser_df = parser_df
        self.classes_paths = self._get_classes_path()
        self.relative_paths = dict(map(lambda x: (x.lower().replace(self.local_path.lower() + os.sep, ''), x.lower()), self.parser_df['File Path'].to_list()))
        self.methods_by_path_and_name = self._get_methods_by_path_and_name()
        self.designite_closest_dict = self.get_designite_closest_dict()
        self.closest_id_dict = self.get_closest_id_dict()

    @staticmethod
    def _get_outpath(project_name, version_name):
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        java_parser = config["JAVA_ANALYSER"]["JavaParser"]
        parser_dir = os.path.join(repository_data, java_parser, project_name)
        parser_dir = Config.get_work_dir_path(parser_dir)
        Config.assert_dir_exists(parser_dir)
        name = project_name
        if version_name:
            name = version_name.replace(os.path.sep, '_')
        path = os.path.join(parser_dir, name)
        return path

    @staticmethod
    def _get_cached(path):
        if not os.path.exists(path):
            return None
        return pd.read_csv(path, delimiter=";")

    @staticmethod
    def _parse_source_code(local_path, cache_path):
        base_dir = Config.get_work_dir_path(Config().config["EXTERNALS"]["BaseDir"])
        runner = os.path.join(base_dir, Config().config["EXTERNALS"]["JavaParser"])
        outdir = tempfile.mkdtemp()
        outpath = os.path.join(outdir, "sourceCodeInformation.csv")
        # commands = ["java", "-jar", runner.replace("\\\\?\\", ""), "-i", local_path, "-o", outdir]
        commands = ["java", '-Xmx4096m', "-jar", runner.replace("\\\\?\\", ""), "-i", local_path, "-o", outdir]
        execute_timeout(commands)
        parser_df = pd.read_csv(outpath, delimiter=";")
        shutil.copyfile(outpath, cache_path)
        shutil.rmtree(outdir)
        return parser_df

    def get_closest_id_dict(self):
        methods_ans = {}
        for _, file_path, package_name, type_name, method_name, parameters, start_line, end_line in self.parser_df[
            ["File Path", 'Package Name', "Type Name", "Method Name", "Parameters", 'Method Beginning Line', 'Method Ending Line']].itertuples():
            lower_name = file_path.lower()
            relative = lower_name.replace(self.local_path.lower() + os.sep, '')
            id = file_path + '@' + package_name + "." + type_name + "." + method_name + parameters
            id = id.lower()
            methods_ans.setdefault(lower_name, []).append((start_line, end_line, id))
            methods_ans.setdefault(relative, []).append((start_line, end_line, id))
        return methods_ans

    def get_closest_id(self, file_name, line=0):
        file_name = os.path.normpath(file_name).lower()
        if file_name not in self.closest_id_dict:
            return None
        for start_line, end_line, id in self.closest_id_dict[file_name]:
            if start_line  - 1 <= line <= end_line + 1:
                return id
        return None

    def get_designite_closest_dict(self):
        methods_ans = {}
        for _, file_path, package_name, type_name, method_name, parameters in self.parser_df[["File Path", 'Package Name', "Type Name", "Method Name", "Parameters"]].itertuples():
            methods_ans[(file_path, package_name, type_name, method_name)] = file_path + '@' + package_name + "." + type_name + "." + method_name + parameters
        return methods_ans

    def get_file_path_by_designite(self, file_path, package_name, type_name, method_name=None):
        if method_name is not None:
            return self.designite_closest_dict.get((file_path, package_name, type_name, method_name))
        return file_path

    def _get_classes_path(self):
            classes_path = dict()
            for row in self.parser_df.itertuples():
                __, file_path, package_name, type_name, __, __, __, __, __, __ = row
                try:
                    key = package_name + "." + type_name
                except Exception:
                    continue
                value = file_path
                classes_path[key.lower()] = value.lower()
            return classes_path

    def _get_methods_by_path_and_name(self):
        methods_by_path_and_name = dict()
        for row in self.parser_df.itertuples():
            __, file_path, package_name, type_name, method_name, parameters, __, __, __, __ = row
            key = (str(file_path).lower(), str(type_name).lower() + "." + str(method_name).lower() + str(parameters))
            value = str(file_path) + '@' + str(package_name) + "." + str(type_name) + "." + str(method_name) + str(parameters)
            methods_by_path_and_name[key] = value
        return methods_by_path_and_name


class JavalangFileAnalyser(FileAnalyser):
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

    @staticmethod
    def _get_cache_name(project_name, version_name):
        config = Config().config
        storing_dir = config['JAVA_ANALYSER']['Javalang']
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
        javalang_parser = config['JAVA_ANALYSER']['Javalang']
        out_dir = os.path.join(repository_data, javalang_parser, project_name)
        Config.assert_dir_exists(out_dir)
        out_path = os.path.join(out_dir, version_name) + ".csv"
        if os.path.exists(out_path):
            return pd.read_csv(out_path, sep=';')
        columns = ["method_id", "file_name", "method_name", "start_line", "end_line"]
        values = list(map(lambda m: [m.id, m.file_name, m.method_name, m.start_line, m.end_line], methods))
        df = pd.DataFrame(values, columns=columns)
        df.to_csv(out_path, index=False, sep=';')
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
