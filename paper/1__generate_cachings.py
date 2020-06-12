import logging

import os
import sys
from multiprocessing import Pool

sys.path.append("..")
from config import Config
from data_extractor import DataExtractor
from projects import ProjectName


done = [
]


def execute(project):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger('success')
    failure_log = logging.getLogger('failure')

    general_log.info("Extracting project {}...".format(project.github()))

    try:
        DataExtractor(project)
    except Exception as e:
        failure_log.exception("Failed to extract {0}.".format(
            project.github()))
        return e
    success_log.info("Succeeded to extract {0}.".format(project.github()))
    return


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
        self.success_log = logging.getLogger('success')
        self.failure_log = logging.getLogger('failure')

    def _set_loggers_level(self):
        self.general_log.setLevel(logging.INFO)
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
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(1)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(1)_failure.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)


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
        ris = p.map(execute, projects)
        print(ris)
