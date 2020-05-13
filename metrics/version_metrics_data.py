import os
import pdb
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from config import Config


class Data(ABC):
    def __init__(self, data_type, project, version, data):
        self.path = self._get_path(data_type, project, version)
        if data is None:
            self.data = self._read_data_to_df()
        else:
            self.data = self._convert_to_df(data)

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

    @abstractmethod
    def store(self):
        self.data.to_csv(self.path, index=False)

    @staticmethod
    def _convert_to_df(data):
        df = pd.DataFrame(data).T.reset_index()
        df.rename(columns={"index": "id"}, inplace=True)
        return df


class CompositeData(Data):
    def __init__(self):
        self.data_collection = []

    def store(self):
        for data in self.data_collection:
            data.store()

    def add(self, data):
        self.data_collection.append(data)


class CheckstyleData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("checkstyle", project, version, data)

    def store(self):
        super().store()


class DesigniteDesignSmellsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_design", project, version, data)

    def store(self):
        super().store()


class DesigniteImplementationSmellsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_implementation", project, version, data)

    def store(self):
        super().store()


class DesigniteOrganicTypeSmellsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_type_organic", project, version, data)

    def store(self):
        super().store()


class DesigniteOrganicMethodSmellsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_method_organic", project, version, data)

    def store(self):
        super().store()


class DesigniteTypeMetricsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_type_metrics", project, version, data)

    def store(self):
        super().store()


class DesigniteMethodMetricsData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("designite_method_metrics", project, version, data)

    def store(self):
        super().store()


class SourceMonitorFilesData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("source_monitor_files", project, version, data)

    def store(self):
        super().store()


class SourceMonitorData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("source_monitor", project, version, data)

    def store(self):
        super().store()


class CKData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("ck", project, version, data)

    def store(self):
        super().store()


class MoodData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("mood", project, version, data)

    def store(self):
        super().store()

class HalsteadData(Data):
    def __init__(self, project, version, data=None):
        super().__init__("halstead", project, version, data)

    def store(self):
        super().store()
