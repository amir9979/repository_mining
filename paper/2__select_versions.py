import logging

import os
import shutil
import sys
import traceback
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

sys.path.append("..")
from config import Config
from data_extractor import DataExtractor
from projects import ProjectName, Project


done = [
]


def select_versions(project_ref):
    index, project = project_ref[0], project_ref[1]
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    general_log.info("{0}:{1}".format(str(index), project.github()))
    extractor = DataExtractor(project)
    try:
        extractor.choose_versions(version_num=5, algorithm="quadratic", strict="true", version_type="all")
        success_log.info("quadratic | Succeeded to select {0}.".format(project.github()))
    except Exception as e:
        failure_log.error("quadratic | Failed to select {0}.".format(project.github()))
        failure_verbose_log.exception("quadratic | Failed to select {0}.".format(project.github()))

    try:
        extractor.choose_versions(version_num=5, algorithm="bin", strict="false", version_type="all")
        success_log.info("bin | Succeeded to select {0}.".format(project.github()))
    except Exception as e:
        failure_log.error("bin | Failed to select {0}.".format(project.github()))
        failure_verbose_log.exception("bin | Failed to select {0}.".format(project.github()))


def organize_quadratic_versions(project: ProjectName):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    general_log.info("organizing quadratic versions for {0}".format(project.github()))

    try:
        data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsQuadratic']
        path = os.path.join(data, selected, project.github() + ".csv")
        in_path = Config.get_work_dir_path(path)
        versions = "versions"
        Path(versions).mkdir(parents=True, exist_ok=True)
        dest_path = os.path.join(versions, project.github() + ".csv")
        if os.path.exists(in_path):
            shutil.copy(in_path, dest_path)
        success_log.info("organize | quadratic | Succeeded to organize {0}".format(project.github()))
        return path
    except Exception as e:
        failure_log.error("organize | quadratic | Failed to organize {0}".format(project.github()))
        failure_verbose_log.exception("organize | quadratic | Failed to organize {0}".format(project.github()))


def organize_bin_versions(project: Project):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    general_log.info("organizing bin versions for {0}".format(project.github()))
    try:
        data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsBin']
        path = os.path.join(data, selected, project.github() + ".csv")
        in_path = Config.get_work_dir_path(path)
        versions = "versions"
        Path(versions).mkdir(parents=True, exist_ok=True)
        dest_path = os.path.join(versions, project.github() + ".csv")
        if os.path.exists(in_path):
            df = pd.read_csv(in_path)
            df.head(8).drop(columns=["start", "step", "stop"]).to_csv(dest_path, index=False)

        success_log.info("organize | bin | Succeeded to organize {0}".format(project.github()))
        return path

    except Exception as e:
        failure_log.error("organize | bin | Failed to organize {0}".format(project.github()))
        failure_verbose_log.exception("organize | bin | Failed to organize {0}".format(project.github()))


class CreateLoggers:
    def __init__(self):
        self._get_loggers()
        self._set_loggers_level()
        self._create_formatters()
        self._create_handlers()
        self._set_formatters_to_handlers()
        self._set_handlers_levels()
        self._set_handlers_to_loggers()

    def _get_loggers(self):
        self.general_log = logging.getLogger(__name__)
        self.summary_log = logging.getLogger('summary')
        self.success_log = logging.getLogger('success')
        self.failure_log = logging.getLogger('failure')
        self.failure_verbose_log = logging.getLogger('failure_verbose')

    def _set_loggers_level(self):
        self.general_log.setLevel(logging.INFO)
        self.summary_log.setLevel(logging.INFO)
        self.success_log.setLevel(logging.INFO)
        self.failure_log.setLevel(logging.ERROR)
        self.failure_verbose_log.setLevel(logging.ERROR)

    def _create_formatters(self):
        self.console_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(message)s'
        )

        self.file_formatter = logging.Formatter(
            '%(asctime)s | %(message)s'
        )

    def _create_handlers(self):
        self.console = logging.StreamHandler()
        paper_dir = Config.get_work_dir_path(os.path.join("paper", "logs"))
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(2)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(2)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(2)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(2)_failure_verbose.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.summary_file.setFormatter(self.file_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)
        self.failure_verbose_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.summary_file.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)
        self.failure_verbose_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.summary_log.addHandler(self.summary_file)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)
        self.failure_verbose_log.addHandler(self.console)
        self.failure_verbose_log.addHandler(self.failure_verbose_file)


if __name__ == "__main__":
    CreateLoggers()
    # projects = list(ProjectName)
    # projects = list(filter(lambda x: x not in done, projects))
    projects = [
        ProjectName.CommonsBeanUtils.value,
        ProjectName.CommonsNet.value,
        ProjectName.Continuum.value,
        ProjectName.Bahir.value
    ]

    with Pool() as p:
         p.map(select_versions, list(enumerate(projects)))
         p.map(organize_bin_versions, projects)
         # p.map(organize_quadratic_versions, projects)
