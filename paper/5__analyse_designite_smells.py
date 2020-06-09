import logging
from pathlib import Path

import functools
import os
import traceback
from multiprocessing import Pool

import pandas as pd

from config import Config
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataName
from projects import ProjectName


done = [
]


def build_dataset(version, project, slog, flog, fvlog):
    print("building {0}:{1}".format(project.github(), version))
    try:
        db = DataBuilder(project, version)
        db.append(DataName.GodClass)
        db.append(DataName.ClassDataShouldBePrivate)
        db.append(DataName.ComplexClass)
        db.append(DataName.LazyClass)
        db.append(DataName.RefusedBequest)
        db.append(DataName.SpaghettiCode)
        db.append(DataName.SpeculativeGenerality)
        db.append(DataName.DataClass)
        db.append(DataName.BrainClass)
        db.append(DataName.LargeClass)
        db.append(DataName.SwissArmyKnife)
        db.append(DataName.AntiSingleton)
        db.append(DataName.FeatureEnvy)
        db.append(DataName.LongMethod_Organic)
        db.append(DataName.LongParameterList_Organic)
        db.append(DataName.MessageChain)
        db.append(DataName.DispersedCoupling)
        db.append(DataName.IntensiveCoupling)
        db.append(DataName.ShotgunSurgery)
        db.append(DataName.BrainMethod)
        db.append(DataName.Bugged)
        classes_df, methods_df = db.build()
        print("succeeded to build {0}:{1}\n".format(
            project.github(),
            version))
        slog.write("succeeded to build {0}:{1}\n".format(
            project.github(),
            version))
        return classes_df
    except Exception as e:
        print("failed to build {0}:{1}\n".format(
            project.github,
            version))
        flog.write("failed to build {0}:{1}\n".format(
            project.github,
            version))
        fvlog.write("failed to build {0}:{1}\n {2}\n{3}\n\n").format(
                project.github(),
                version,
                e,
                traceback.format_exc())
        return None

def execute(project):
    dir = Config.get_work_dir_path(os.path.join("paper", "logs"))
    slog = open(os.path.join(dir, "(4)_success_xm.log"), "a")
    flog = open(os.path.join(dir, "(4)_failed_xm.log"), "a")
    fvlog = open(os.path.join(dir, "(4)_failed_verbose_xm.log"), "a")

    versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
    versions_path = os.path.join(versions_dir, project.github() + ".csv")
    versions = pd.read_csv(versions_path)['version'].to_list()
    build = functools.partial(build_dataset,
                                project=project,
                                slog=slog,
                                flog=flog,
                                fvlog=fvlog)

    dfs = list(map(build, versions))

    slog.close()
    flog.close()
    fvlog.close()

    if None in dfs:
        print("project " + project.github() + " failed")
        return

    df = pd.concat(dfs, axis=0, ignore_index=False)

    dir = Config.get_work_dir_path(os.path.join("paper", "datasets"))
    Path(dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(dir, project.github()+"_fowler" + ".csv")
    df.to_csv(path)


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
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(5)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(5)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(5)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(5)_failure_verbose.log"), "a")

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
    projects = list(ProjectName)
    projects = list(filter(lambda x: x not in done, projects))
    with Pool() as p:
        ris = p.map(execute, projects)
        print(ris)
