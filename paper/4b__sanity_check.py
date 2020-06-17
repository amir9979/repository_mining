import logging
import sys
from multiprocessing import Pool

import pandas as pd

import functools
import os

sys.path.append("..")
from config import Config
from projects import ProjectName


def check_path(component, project, version, path):
    component_path = os.path.join(path, component)
    if not os.path.exists(component_path):
        logging.getLogger("failure").error("{0} | {1} | {2} not found.".format(
            project.github(),
            version,
            component
        ))
        return False
    logging.getLogger("success").info("{0} | {1} | {2} found.".format(
        project.github(),
        version,
        component
    ))
    return True


def sanity_check(version, project):
    repository_data = Config().config["CACHING"]["RepositoryData"]
    metrics_dir = Config().config["VERSION_METRICS"]["MetricsDir"]
    repository_data = os.path.join(repository_data, metrics_dir)
    repository_data = Config.get_work_dir_path(repository_data)
    path = os.path.join(repository_data, project.github(), version)
    components = [
        "bugged.csv",
        "checkstyle.csv",
        "ck.csv",
        "designite_design.csv",
        "designite_implementation.csv",
        "designite_method_metrics.csv",
        "designite_method_organic.csv",
        "designite_type_metrics.csv",
        "designite_type_organic.csv",
        "halstead.csv"
    ]

    if not os.path.exists(path) or not os.path.isdir(path):
        logging.getLogger("failure").error("{0} | {1} | Path not found.".format(
            project.github(),
            version
        ))
        return False

    check_path_fn = functools.partial(check_path,
                                      project=project,
                                      version=version,
                                      path=path)

    succeeded = list(map(check_path_fn, components))

    return all(succeeded)


def execute(project):
    summary_log = logging.getLogger('summary')

    versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
    versions_path = os.path.join(versions_dir, project.github() + ".csv")
    try:
        versions = pd.read_csv(versions_path)['version'].to_list()
    except Exception:
        logging.getLogger("failure").error("{0} | Project does not exist.".format(project.github()))
        summary_log.info("Project {0} failed.".format(project.github()))
        return

    extract = functools.partial(sanity_check,
                                project=project)
    success_summary = list(map(extract, versions))
    if all(success_summary):
        summary_log.info("Project {0} succeeded.".format(project.github()))
    else:
        summary_log.info("Project {0} failed.".format(project.github()))


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

    def _set_loggers_level(self):
        self.general_log.setLevel(logging.INFO)
        self.summary_log.setLevel(logging.INFO)
        self.success_log.setLevel(logging.INFO)
        self.failure_log.setLevel(logging.ERROR)

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
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(4b)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(4b)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(4b)_failure.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.summary_file.setFormatter(self.file_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.summary_file.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.summary_log.addHandler(self.summary_file)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)


if __name__ == "__main__":
    CreateLoggers()

    projects = list(ProjectName)
    with Pool() as p:
        ris = p.map(execute, projects)
        print(ris)
