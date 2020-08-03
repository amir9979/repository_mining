import sys
import os

import pandas as pd

from config import Config
from projects import ProjectName


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
    columns = [
        'project',
        'version',
        'original_num_files_per_version',
        'original_num_defective_files_per_version',
        'original_training_num_files',
        'original_testing_num_files',
        'original_training_num_defective_files',
        'original_testing_num_defective_files',
        'metric_name',
        'num_training_files',
        'num_testing_files',
        'num_training_defective_files',
        'num_testing_defective_files',
        'defective_ratio'
    ]

    try:
        versions_path = Config.get_work_dir_path(os.path.join("paper", "versions", project.github() + ".csv"))
        versions_df = pd.read_csv(versions_path)
        versions = list(map(lambda x: x[0], versions_df.values))
        repository_path = Config().config["CACHING"]["RepositoryData"]
        path = Config.get_work_dir_path(os.path.join(
            repository_path, "apache_versions", project.github(), project.jira() + ".csv"))
        versions_info_df = pd.read_csv(path, sep=';')
        cond = versions_info_df.version_name.isin(versions)
        versions_info_df = versions_info_df[cond].reset_index().drop('index', axis=1)
        original_training_num_files = sum(versions_info_df.iloc[:-1,:]['#commited_files_in_version'])
        original_training_num_defective_files = sum(versions_info_df.iloc[:-1,:]['#commited_files_in_version'])
        original_testing_num_files = versions_info_df.iloc[-1,:]['#commited_files_in_version']
        original_testing_num_defective_files = versions_info_df.iloc[-1,:]['#bugged_files_in_version']

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

        for row in scores_df.itertuples():
            __, estimator, configuration, precision, recall, f1_measure, auc_roc, brier_score, metric_configuration = row
            cond = num_defects_df['metric_name'] == metric_configuration
            __, training, training_defective, testing, testing_defective = num_defects_df.loc[cond].iloc[0, :]
            for inner_row in versions_info_df.itertuples():
                __, version, num_files, num_defective_files, defective_ratio, __, __, __, __, __ = inner_row

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
        return info_df
    except Exception:
        return pd.DataFrame(columns=columns)


projects = list(ProjectName)
data_list = list(map(execute, projects))
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "defects", "data.csv"))
data = pd.concat(data_list, axis=0)
data.to_csv(path, index=False)

