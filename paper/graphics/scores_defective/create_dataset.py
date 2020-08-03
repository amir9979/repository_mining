import os

import pandas as pd
from tqdm import tqdm

from config import Config
from projects import ProjectName


def get_scores(metric, metric_name, project_name):
    path = Config.get_work_dir_path(
        os.path.join("paper", "analysis", metric, project_name, "scores.csv"))
    scores_df = pd.read_csv(path, sep=';')
    scores_df['metric_configuration'] = metric_name
    return scores_df


def get_num_defects(metric, metric_name, project_name):
    training_path = Config.get_work_dir_path(
        os.path.join("paper", "analysis", metric, project_name, "dataset", "training.csv"))
    testing_path = Config.get_work_dir_path(
        os.path.join("paper", "analysis", metric, project_name, "dataset", "testing.csv"))

    training_df = pd.read_csv(training_path).dropna()
    testing_df = pd.read_csv(testing_path).dropna()
    training_defective_files = training_df.apply(lambda x: x['Bugged'], axis=1)
    testing_defective_files = testing_df.apply(lambda x: x['Bugged'], axis=1)
    num_defects_dict = {
        'metric_name': metric_name,
        'num_training_files': len(training_df.index),
        'num_training_defective_files': len(training_defective_files[training_defective_files].index),
        'num_testing_files': len(testing_df.index),
        'num_testing_defective_files': len(testing_defective_files[testing_defective_files].index)
    }

    return num_defects_dict


columns = [
    'project',
    'version',
    'version_num',
    'feature_selection',
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
    'precision',
    'recall',
    'f1_measure',
    'auc_roc',
    'brier-score'
]
info_df = pd.DataFrame(columns=columns)

projects = list(ProjectName)
for project in tqdm(projects, total=len(projects), unit="Project"):
    print("{0}\n".format(project.github()))
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
        original_training_num_files = sum(versions_info_df.iloc[:-1, :]['#commited_files_in_version'])
        original_training_num_defective_files = sum(versions_info_df.iloc[:-1, :]['#commited_files_in_version'])
        original_testing_num_files = versions_info_df.iloc[-1, :]['#commited_files_in_version']
        original_testing_num_defective_files = versions_info_df.iloc[-1, :]['#bugged_files_in_version']

        scores_df_list = list()
        scores_df_list.append(get_scores("designite", "Designite", project.github()))
        scores_df_list.append(get_scores("designite_fowler", "Designite + Fowler", project.github()))
        scores_df_list.append(get_scores("designite_fowler_traditional", "Traditional + Designite + Fowler", project.github()))
        scores_df_list.append(get_scores("designite_traditional", "Traditional + Designite", project.github()))
        scores_df_list.append(get_scores("fowler", "Fowler", project.github()))
        scores_df_list.append(get_scores("fowler_traditional", "Traditional + Fowler", project.github()))
        scores_df_list.append(get_scores("traditional", "Traditional", project.github()))

        scores_df = pd.concat(scores_df_list, axis=0)

        num_defects_dict_list = list()
        num_defects_dict_list.append(get_num_defects("designite", "Designite", project.github()))
        num_defects_dict_list.append(get_num_defects("designite_fowler", "Designite + Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("designite_fowler_traditional", "Traditional + Designite + Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("designite_traditional", "Traditional + Designite", project.github()))
        num_defects_dict_list.append(get_num_defects("fowler", "Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("fowler_traditional", "Traditional + Fowler", project.github()))
        num_defects_dict_list.append(get_num_defects("traditional", "Traditional", project.github()))

        num_defects_df = pd.DataFrame(num_defects_dict_list)

        info_dict = dict()

        for row in tqdm(scores_df.itertuples(), total=len(scores_df), unit="Score"):
            __, estimator, configuration, feature_selection, precision, recall, f1_measure, auc_roc, brier_score, metric_configuration = row
            cond = num_defects_df['metric_name'] == metric_configuration
            __, training, training_defective, testing, testing_defective = num_defects_df.loc[cond].iloc[0, :]
            version_num = 0
            for inner_row in versions_info_df.itertuples():
                __, version, num_files, num_defective_files, defective_ratio, __, __, __, __, __ = inner_row

                info_dict['project'] = project.github()
                info_dict['version'] = version
                info_dict['version_num'] = version_num
                version_num += 1
                info_dict['feature_selection'] = feature_selection
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
                info_dict['precision'] = precision
                info_dict['recall'] = recall
                info_dict['f1_measure'] = f1_measure
                info_dict['auc_roc'] = auc_roc
                info_dict['brier_score'] = brier_score
                info_df = info_df.append(info_dict, ignore_index=True)

    except Exception as e:
        continue


path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores_defective", "data.csv"))
info_df.to_csv(path, index=False, sep=';')



