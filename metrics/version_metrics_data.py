import os
from abc import ABC, abstractmethod
from enum import Enum
from itertools import tee
from pathlib import Path
from collections import OrderedDict

import pandas as pd

from config import Config
from metrics.version_metrics_name import DataName
from metrics.version_metrics_name import DataType


class Data(ABC):
    def __init__(self, project, version):
        self.path = self._get_path(self.data_type, project, version)
        if self.raw_data is None:
            self.data = self._read_data_to_df()
        else:
            self.data = self._convert_to_df(self.raw_data)

    @staticmethod
    def _get_path(data_type, project, version):
        config = Config().config
        repository_data = config['CACHING']['RepositoryData']
        metrics_dirname = config['VERSION_METRICS']['MetricsDir']
        metrics_dir = os.path.join(repository_data, metrics_dirname)
        metrics_dir_path = Config().get_work_dir_path(metrics_dir)
        version_dir_path = os.path.join(metrics_dir_path, project, version)
        Path(version_dir_path).mkdir(parents=True, exist_ok=True)
        path = os.path.join(version_dir_path, data_type + ".csv")
        return path

    def _read_data_to_df(self):
        data = pd.read_csv(self.path)
        return data

    @staticmethod
    def _convert_to_df(data):
        df = pd.DataFrame(data).T.reset_index()
        df.rename(columns={"index": "id"}, inplace=True)
        return df

    def store(self):
        self.data.dropna(inplace=True)
        self.data.to_csv(self.path, index=False)

    @abstractmethod
    def build(self, values) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        id = df.columns[0]
        return df[[id] + values]


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
        self.add(CheckstyleData(project, version)) \
            .add(DesigniteDesignSmellsData(project, version)) \
            .add(DesigniteImplementationSmellsData(project, version)) \
            .add(DesigniteOrganicTypeSmellsData(project, version)) \
            .add(DesigniteOrganicMethodSmellsData(project, version)) \
            .add(DesigniteTypeMetricsData(project, version)) \
            .add(DesigniteMethodMetricsData(project, version)) \
            .add(CKData(project, version)) \
            .add(MoodData(project, version)) \
            .add(HalsteadData(project, version))
        return self

    def build(self, data, column_names):
        files_dfs = []
        classes_dfs = []
        methods_dfs = []
        for data_type, data_values in data.items():
            df = self.data_collection\
                     .get(data_type)\
                     .build(data_values, column_names)
            if "Method" in df.columns:
                methods_dfs.append(df.drop(columns="Package"))
            elif "Class" in df.columns:
                classes_dfs.append(df.drop(columns="Package"))
            else:
                files_dfs.append(df)
        classes_df = None
        methods_df = None

        if classes_dfs:
            classes_df = classes_dfs.pop(0)
            while classes_dfs:
                classes_df = classes_df.merge(classes_dfs.pop(0), on=['File', 'Class'], how='outer')

        if files_dfs:
            classes_df = files_dfs.pop(0) if classes_df.empty else classes_df
            while files_dfs:
                classes_df = classes_df.merge(files_dfs.pop(0), on=['File'], how='outer')

        if methods_dfs:
            methods_df = methods_dfs.pop(0)
            while methods_dfs:
                method_df = methods_dfs.pop(0)
                methods_df = methods_df.merge(method_df, on=['File', 'Class', 'Method'], how='outer')

        return classes_df, methods_df


class CheckstyleData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.CheckstyleDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
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
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id = tee(id, 3)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('.')[-1], classes_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteImplementationSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteImplementationSmellsDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1], methods_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
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
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id = tee(id, 3)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('.')[-1], classes_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteOrganicMethodSmellsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteOrganicMethodSmellsDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1], methods_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
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
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id = tee(id, 3)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('.')[-1], classes_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DesigniteMethodMetricsData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.DesigniteMethodMetricsDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1], methods_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
        df.insert(0, 'Class',  classes)
        df.insert(0, 'Package',  packages)
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class SourceMonitorFilesData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.SourceMonitorFilesDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values):
        df = super().build(values)
        return df


class SourceMonitorData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.SourceMonitorDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values):
        df = super().build(values)
        return df


class CKData(Data):
    def __init__(self, project, version, data=None):
        self.data_type = DataType.CKDataType.value
        self.raw_data = data
        super().__init__(project, version)
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files_id, packages_id, classes_id, methods_id = tee(id, 4)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        packages = pd.Series(list(map(lambda x: '.'.join(x[1].split('@')[1].split('.')[:-2]), packages_id))).values
        classes = pd.Series(list(map(lambda x: x[1].split('@')[1].split('.')[:-1][-1], classes_id))).values
        methods = pd.Series(list(map(lambda x: x[1].split('.')[-1].split('(')[0], methods_id))).values
        df = df.drop(columns='id')
        df.insert(0, 'Method', methods)
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
        pass

    def build(self, values, column_names):
        df = super().build(values)
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
        pass

    def build(self, values, column_names):
        df = super().build(values)
        id = df['id'].iteritems()
        files = pd.Series(list(map(lambda x: x[1], id))).values
        df = df.drop(columns='id')
        df.insert(0, 'File',  files)
        df = df.rename(columns=column_names)
        return df


class DataBuilder:
    def __init__(self, project, version):
        self.data_collection = CompositeData().add_all(project, version)
        self.metrics = pd.DataFrame(columns=['data_value', 'data_type', 'data_column'])

    def append(self, metric_name: DataName):
        data_value = metric_name.name
        data_type = metric_name.value[1]
        data_column = metric_name.value[2]
        data_dict = {'data_value': data_value, 'data_type': data_type, 'data_column': data_column}
        self.metrics = self.metrics.append(data_dict, ignore_index=True)

    def build(self):
        self.metrics = self.metrics.drop_duplicates().reset_index(drop=True)
        data = self.metrics.groupby('data_type')['data_column'] \
            .apply(lambda x: x.values.tolist()).to_dict()
        column_names = dict(zip(self.metrics['data_column'], self.metrics['data_value']))
        df = self.data_collection.build(data, column_names)

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
