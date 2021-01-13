import os
from abc import ABC, abstractmethod
from itertools import tee
from pathlib import Path
from collections import OrderedDict

import pandas as pd

from config import Config
from metrics.version_metrics_name import DataNameEnum
from metrics.version_metrics_name import DataType
from projects import ProjectName, Project
import gc
from typing import List


class Data(ABC):
    def __init__(self, project: Project, version: str):
        self.path = self._get_path(self.data_type, project, version)
        self.describe_path = self.path.replace(".csv", '_describe.csv')
        if self.raw_data is None:
            try:
                self.data = self._read_data_to_df()
            except Exception as e:
                pass
        else:
            self.data = self._convert_to_df(self.raw_data)

    @staticmethod
    def _get_path(data_type, project, version):
        config = Config().config
        repository_data = config['CACHING']['RepositoryData']
        metrics_dirname = config['VERSION_METRICS']['MetricsDir']
        metrics_dir = os.path.join(repository_data, metrics_dirname)
        metrics_dir_path = Config().get_work_dir_path(metrics_dir)
        version_dir_path = os.path.join(metrics_dir_path, project.github_name, version)
        Path(version_dir_path).mkdir(parents=True, exist_ok=True)
        path = os.path.join(version_dir_path, data_type + ".csv")
        return path

    def _read_data_to_df(self):
        data = pd.read_csv(self.path, sep=';')
        return data

    @staticmethod
    def _convert_to_df(data):
        df = pd.DataFrame(data).T.reset_index()
        df.rename(columns={"index": "id"}, inplace=True)
        if 'id' in df.columns.values.tolist():
            df = df[df.id.notnull()]
            df['id'] = df['id'].apply(os.path.normpath)
        if 'Method_ids' in df.columns.values.tolist():
            df = df[df.Method_ids.notnull()]
            df['Method_ids'] = df['Method_ids'].apply(os.path.normpath)
        return df

    def set_raw_data(self, raw):
        self.raw_data = raw
        self.data = self._convert_to_df(raw)

    def store(self):
        # self.data.dropna(inplace=True)
        self.data.to_csv(self.path, index=False, sep=';')
        self.data.describe(include = 'all').to_csv(self.describe_path, index=False, sep=';')

    @abstractmethod
    def build(self, values, column_names) -> pd.DataFrame:
        df = pd.read_csv(self.path, sep=';')
        id = df.columns[0]
        metrics = list(filter(lambda x: x in df.columns, [id] + values))
        return df[metrics].rename(columns=column_names)


    @staticmethod
    def get_all_datas(project, version):
        for s in Data.__subclasses__():
            if s.__name__ == "CompositeData":
                # skip Compisite
                continue
            yield s(project, version)


class CompositeData(Data):
    def __init__(self):
        self.data_collection = OrderedDict()

    def store(self):
        for data in self.data_collection.values():
            data.store()

    def add(self, data: Data):
        self.data_collection[data.data_type] = data
        return self

    def add_all(self, project, version):
        for d in Data.get_all_datas(project, version):
            self.add(d)
        return self

    def merge(self, merge_on, dfs):
        data = dict()
        df = dfs.pop(0)
        for ind, row in df.iterrows():
            d = row.to_dict()
            key = tuple(map(d.get, merge_on))
            data[key] = d
        while dfs:
            gc.collect()
            iter_df = dfs.pop(0)
            for ind, row in iter_df.iterrows():
                d = row.to_dict()
                key = tuple(map(d.get, merge_on))
                data.setdefault(key, dict()).update(d)
            # f, path = tempfile.mkstemp()
            # os.close(f)
            # os.remove(path)
            # iter_df.to_csv(path, index_label=False)
            # del(iter_df)
            # for r in pd.read_csv(path, chunksize=1000):
            #     df = df.merge(r, on=merge_on, how='outer')
            #     gc.collect()
        return pd.DataFrame(list(data.values()))

    def build(self, data, column_names):
        files_dfs = []
        classes_dfs = []
        methods_dfs = []
        for data_type, data_values in data.items():
            if self.data_collection.get(data_type) is None:
                continue
            try:
                df = self.data_collection.get(data_type).build(data_values, column_names)
            except:
                import traceback
                traceback.print_exc()
                print(f"failed to build {data_type}")
                continue
            if "Method_ids" in df.columns:
                methods_dfs.append(df.drop(["File", "Class", "Package", "Method"], errors='ignore'))
            elif "Class" in df.columns:
                classes_dfs.append(df.drop(["Package", "Method", 'Method_ids'], axis=1, errors='ignore'))
            elif "File" in df.columns:
                files_dfs.append(df.drop(["Package", "Method", 'Method_ids'], axis=1, errors='ignore'))
        classes_df = None
        methods_df = None

        if classes_dfs:
            classes_df = classes_dfs.pop(0)
            classes_df['File'] = classes_df.File.astype(str)
            classes_df['Class'] = classes_df.Class.astype(str)
            classes_df['File'] = classes_df['File'].str.lower()
            classes_df['Class'] = classes_df['Class'].str.lower()
            classes_df['File'] = classes_df['File'].apply(lambda x: os.path.normpath(x).lower())
            while classes_dfs:
                gc.collect()
                other = classes_dfs.pop(0)
                other['File'] = other.File.astype(str)
                other['Class'] = other.Class.astype(str)
                other['File'] = other['File'].str.lower()
                other['Class'] = other['Class'].str.lower()
                other['File'] = other['File'].apply(lambda x: os.path.normpath(x).lower())
                classes_df = classes_df.merge(other, on=['File', 'Class'], how='outer')

        if files_dfs:
            if classes_df is None:
                classes_df = files_dfs.pop(0)
                classes_df['File'] = classes_df.File.astype(str)
                classes_df['File'] = classes_df['File'].str.lower()
                classes_df['File'] = classes_df['File'].apply(lambda x: os.path.normpath(x).lower())
            while files_dfs:
                gc.collect()
                other = files_dfs.pop(0)
                other['File'] = other.File.astype(str)
                other['File'] = other['File'].str.lower()
                other['File'] = other['File'].apply(lambda x: os.path.normpath(x).lower())
                classes_df = classes_df.merge(other, on=['File'], how='outer')

        if methods_dfs:
            methods_df = methods_dfs.pop(0)
            methods_df = methods_df.drop(["File", "Class", "Package", "Method"], axis=1, errors='ignore')
            methods_df['Method_ids'] = methods_df.Method_ids.astype(str)
            methods_df['Method_ids'] = methods_df['Method_ids'].str.lower()
            methods_df['Method_ids'] = methods_df['Method_ids'].apply(lambda x: os.path.normpath(x).lower())
            while methods_dfs:
                gc.collect()
                method_df = methods_dfs.pop(0)
                method_df = method_df.drop(["File", "Class", "Package", "Method"], axis=1, errors='ignore')
                method_df['Method_ids'] = method_df.Method_ids.astype(str)
                method_df['Method_ids'] = method_df['Method_ids'].str.lower()
                method_df['Method_ids'] = method_df['Method_ids'].apply(lambda x: os.path.normpath(x).lower())
                methods_df = methods_df.merge(method_df, on=['Method_ids'], how='outer')

        return classes_df, methods_df


class BuggedData(Data):
    def __init__(self, project: Project, version, data=None):
        self.data_type = DataType.BuggedDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files = pd.Series(list(map(lambda x: x[1], id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File', files)
        df = df.rename(columns=column_names)
        return df


class BuggedMethodData(Data):
    def __init__(self, project: Project, version, data=None):
        self.data_type = DataType.BuggedMethodsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].apply(os.path.normpath).iteritems()
        methods = pd.Series(list(map(lambda x: x[1], id))).values
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df = df.rename(columns=column_names)
        return df


class CheckstyleData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.CheckstyleDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteDesignSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteDesignSmellsDataType.value
        self.raw_data = data
        super(DesigniteDesignSmellsData, self).__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()        
        files_id, packages_id, classes_id = tee(id, 3)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteImplementationSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteImplementationSmellsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteOrganicTypeSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteOrganicTypeSmellsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        packages_id, classes_id,files_id = tee(id, 3)
        
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteOrganicMethodSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteOrganicMethodSmellsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        packages_id, classes_id, methods_id,files_id = tee(id, 4)
        
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteTypeMetricsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteTypeMetricsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        packages_id, classes_id,files_id = tee(id,3)
        
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteMethodMetricsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteMethodMetricsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        packages_id, classes_id, methods_id = tee(id, 3)
        
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df = df.rename(columns=column_names)
        return df


class SourceMonitorFilesData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.SourceMonitorFilesDataType.value
        self.raw_data = data
        super().__init__(project, version)


    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class SourceMonitorData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.SourceMonitorDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "Method_ids"})


class CKData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.CKDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class MoodData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.MoodDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files = pd.Series(list(map(lambda x: x[1], id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class HalsteadData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.HalsteadDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files = pd.Series(list(map(lambda x: x[1], id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class JasomeFilesData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.JasomeFilesDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class JasomeMoodData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.JasomeMoodDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class JasomeCKData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.JasomeCKDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class JasomeLKData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.JasomeLKDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class JasomeMethodsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.JasomeMethodsDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        ids = df['id'].apply(os.path.normpath)
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Method_ids', ids)
        df.insert(0, 'Class', classes)
        df.insert(0, 'Package', packages)
        df.insert(0, 'File', files)
        df = df.rename(columns=column_names)
        return df


class DataBuilder:
    def __init__(self, project: ProjectName, version):
        self.data_collection = CompositeData().add_all(project, version)
        self.metrics = pd.DataFrame(columns=['data_value', 'data_type', 'data_column'])

    def append(self, metric_name: DataNameEnum):
        self.metrics = self.metrics.append(metric_name.value.as_data_dict(), ignore_index=True)

    def extend(self, metrics: List[DataNameEnum]):
        for m in metrics:
            self.append(m)

    def add_data_types(self, data_types: List[DataType]):
            self.extend(DataNameEnum.get_data_names_by_type(data_types))

    def build(self):
        self.metrics = self.metrics.drop_duplicates().reset_index(drop=True)
        data = self.metrics.groupby('data_type')['data_column'] \
            .apply(lambda x: x.values.tolist()).to_dict()
        column_names = dict(zip(self.metrics['data_column'], self.metrics['data_value']))
        return self.data_collection.build(data, column_names)

    def __repr__(self):
        self.metrics = self.metrics.drop_duplicates().reset_index(drop=True)
        output = ""
        if self.metrics.size == 0:
            return "Empty"
        for data_type in self.metrics.data_type.unique():
            output += data_type + "\n"
            cond = self.metrics['data_type'] == data_type
            rows = ["\t" + value[1] for value in self.metrics.loc[cond]['data_value'].iteritems()]
            output += "\n".join(rows)
            output += "\n"
        return output


class ProcessData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.ProcessFilesDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})


class IssuesData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.IssuesFilesDataType.value
        self.raw_data = data
        super().__init__(project, version)

    def build(self, values, column_names):
        df = super().build(values, column_names)
        return df.rename(columns={"id": "File"})
