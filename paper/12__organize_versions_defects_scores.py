import logging
import sys
from multiprocessing import Pool
import functools
import os

import pandas as pd

sys.path.append("..")
from config import Config
from projects import ProjectName


def get_scores(metric, metric_name, project_name):
    path = Config.get_work_dir_path(
        os.path.join("paper", "scores", metric, project_name, "scores.csv"))
    scores_df = pd.read_csv(path)
    scores_df['metric_configuration'] = metric_name
    return scores_df


def get_num_defects(metric, metric_name, project_name):
    training_path = Config.get_work_dir_path(
        os.path.join("paper", "scores", metric, project_name, "training_y.csv"))
    testing_path = Config.get_work_dir_path(
        os.path.join("paper", "scores", metric, project_name, "testing_y.csv"))

    training_df = pd.read_csv(training_path)
    testing_df = pd.read_csv(testing_path)
    num_training_defective_files = len(list(filter(lambda x: x[0] == 1, training_df.values)))
    num_testing_defective_files = len(list(filter(lambda x: x[0] == 1, testing_df.values)))
    num_defects_dict = {
        'metric_name': metric_name,
        'num_training_files': len(training_df),
        'num_training_defective_files': num_training_defective_files,
        'num_testing_files': len(testing_df),
        'num_testing_defective_files': num_testing_defective_files
    }

    return num_defects_dict


def execute(project):
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")
    general_log = logging.getLogger(__name__)

    columns = [
        'project',
        'version',
        'original_num_files_per_version',
        'original_num_defective_files_per_version',
        'original_training_num_files',
        'original_testing_num_files',
        'original_training_num_defective_files',
        'original_testing_num_defective_files',
        'num_training_files',
        'num_testing_files',
        'num_training_defective_files',
        'num_testing_defective_files',
        'defective_ratio',
        'metrics_configuration',
        'estimator',
        'estimator_configuration',
        'measure',
        'value'
    ]

    general_log.info("{0} | Starting Process".format(project.github()))
    try:
        versions_path = Config.get_work_dir_path(os.path.join("paper", "versions", project.github() + ".csv"))
        versions_df = pd.read_csv(versions_path)
        versions = list(map(lambda x: x[0], versions_df.values))
        repository_path = Config().config["CACHING"]["RepositoryData"]
        path = Config.get_work_dir_path(os.path.join(
            repository_path, "apache_versions", project.github(), project.jira() + ".csv"))
        versions_info_df = pd.read_csv(path)
        cond = versions_info_df.version_name.isin(versions)
        versions_info_df = versions_info_df[cond].reset_index().drop('index', axis=1)
        original_training_num_files = sum(versions_info_df.iloc[:-1,:]['#commited_files_in_version'])
        original_training_num_defective_files = sum(versions_info_df.iloc[:-1,:]['#commited_files_in_version'])
        original_testing_num_files = versions_info_df.iloc[-1,:]['#commited_files_in_version']
        original_testing_num_defective_files = versions_info_df.iloc[-1,:]['#bugged_files_in_version']

        scores_df_list = list()
        scores_df_list.append(get_scores("designite", "Designite", project.github()))
        scores_df_list.append(get_scores("fowler", "Fowler", project.github()))
        scores_df_list.append(get_scores("designite_fowler", "Designite + Fowler", project.github()))
        scores_df_list.append(get_scores("traditional", "Traditional", project.github()))
        scores_df_list.append(get_scores("traditional_designite", "Traditional + Designite", project.github()))
        scores_df_list.append(get_scores("traditional_folwer", "Traditional + Fowler", project.github()))
        scores_df_list.append(get_scores("traditional_designite_fowler", "Traditional + Designite + Fowler", project.github()))

        scores_df = pd.concat(scores_df_list, axis=0)

        num_defects_dict_list = list()
        num_defects_dict_list.append(get_num_defects("designite", "Designite", project.github()))
        num_defects_dict_list.append(get_num_defects("fowler", "Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("designite_fowler", "Designite + Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("traditional", "Traditional", project.github()))
        num_defects_dict_list.append(get_num_defects("traditional_designite", "Traditional + Designite", project.github()))
        num_defects_dict_list.append(get_num_defects("traditional_folwer", "Traditional + Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("traditional_designite_fowler", "Traditional + Designite + Fowler", project.github()))

        num_defects_df = pd.DataFrame(num_defects_dict_list)

        info_df = pd.DataFrame(columns=columns)
        info_dict = dict()

        general_log.info("{0} | Extracting info".format(project.github()))
        for row in scores_df.itertuples():
            __, estimator, configuration, precision, recall, f1_measure, auc_roc, brier_score, metric_configuration = row
            cond = num_defects_df['metric_name'] == metric_configuration
            __, training, training_defective, testing, testing_defective = num_defects_df.loc[cond].iloc[0, :]
            for inner_row in versions_info_df.itertuples():
                __, version, num_files, num_defective_files, defective_ratio, __, __, __, __, __ = inner_row
                general_log.info("{0} | {1} | Extracting Version".format(project.github(), version))

                info_dict['project'] = project.github()
                info_dict['version'] = version
                info_dict['original_num_files_per_version'] = num_files
                info_dict['original_num_defective_files_per_version'] = num_defective_files
                info_dict['num_training_files'] = training
                info_dict['num_training_defective_files'] = training_defective
                info_dict['num_testing_files'] = testing
                info_dict['num_testing_defective_files'] = testing_defective
                info_dict['original_training_num_files'] = original_training_num_files
                info_dict['original_testing_num_files'] = original_testing_num_files
                info_dict['original_training_num_defective_files'] = original_training_num_defective_files
                info_dict['original_testing_num_defective_files'] = original_testing_num_defective_files
                info_dict['defective_ratio'] = defective_ratio
                info_dict['metrics_configuration'] = metric_configuration
                info_dict['estimator'] = estimator
                info_dict['estimator_configuration'] = configuration

                info_dict['measure'] = "precision"
                info_dict['value'] = precision
                info_df = info_df.append(info_dict, ignore_index=True)
                info_dict['measure'] = "recall"
                info_dict['value'] = recall
                info_df = info_df.append(info_dict, ignore_index=True)
                info_dict['measure'] = "f1_measure"
                info_dict['value'] = f1_measure
                info_df = info_df.append(info_dict, ignore_index=True)
                info_dict['measure'] = "auc_roc"
                info_dict['value'] = auc_roc
                info_df = info_df.append(info_dict, ignore_index=True)
                info_dict['measure'] = "brier_score"
                info_dict['value'] = brier_score
                info_df = info_df.append(info_dict, ignore_index=True)
        success_log.info("{0} | Info Extraction Succeeded".format(project.github()))
        return info_df
    except Exception:
        failure_log.error("{0} | Info Extraction Failed".format(project.github()))
        failure_verbose_log.exception("{0} | Info Extraction Failed".format(project.github()))
        return pd.DataFrame(columns=columns)

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
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(12)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(12)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(12)_failure_verbose.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)
        self.failure_verbose_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)
        self.failure_verbose_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)
        self.failure_verbose_log.addHandler(self.console)
        self.failure_verbose_log.addHandler(self.failure_verbose_file)


if __name__ == "__main__":
    CreateLoggers()

    projects = list(ProjectName)
    infos_dfs = list(map(execute, projects))
    info_dir = Config.assert_dir_exists(Config.get_work_dir_path(os.path.join("paper", "defect_info")))
    info_path = os.path.join(info_dir, "dataset.csv")
    info_df = pd.concat(infos_dfs, axis=0)
    info_df.to_csv(info_path, index=False)



