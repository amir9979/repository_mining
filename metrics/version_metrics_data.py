import os
from abc import ABC, abstractmethod
from pathlib import Path
from collections import OrderedDict

import pandas as pd

from config import Config


class Data(ABC):
    def __init__(self, project, version, data):
        self.path = self._get_path(self.data_type, project, version)
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

    def store(self):
        self.data.to_csv(self.path, index=False)

    @staticmethod
    def _convert_to_df(data):
        df = pd.DataFrame(data).T.reset_index()
        df.rename(columns={"index": "id"}, inplace=True)
        return df


class CompositeData(Data):
    def __init__(self):
        self.data_collection = OrderedDict()

    def store(self):
        for data in self.data_collection.values():
            data.store()

    def add(self, data):
        self.data_collection[data.data_type] = data


class CheckstyleData(Data):
    data_type = "checkstyle"


class DesigniteDesignSmellsData(Data):
    data_type = "designite_design"


class DesigniteImplementationSmellsData(Data):
    data_type = "designite_implementation"


class DesigniteOrganicTypeSmellsData(Data):
    data_type = "designite_type_organic"


class DesigniteOrganicMethodSmellsData(Data):
    data_type = "designite_method_organic"


class DesigniteTypeMetricsData(Data):
    data_type = "designite_type_metrics"


class DesigniteMethodMetricsData(Data):
    data_type = "designite_method_metrics"


class SourceMonitorFilesData(Data):
    data_type = "source_monitor_files"


class SourceMonitorData(Data):
    data_type = "source_monitor"


class CKData(Data):
    data_type = "ck"


class MoodData(Data):
    data_type = "mood"


class HalsteadData(Data):
    data_type = "halstead"

