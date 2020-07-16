import os
from itertools import product

import pandas as pd
from tqdm import tqdm

from config import Config
from projects import ProjectName


path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores_defective", "data.csv"))
df = pd.read_csv(path)

score_types = ["precision", "recall", "f1_measure", "auc_roc", "brier_score"]
features_methods = ["all", "chi2_20p", "chi2_50p", "f_classif_20", "f_classif_50", "mutual_info_classif_20p",
                    "mutual_info_classif_50p", "recursive_elimination", "mutual_info_classif_50p",
                    "recursive_elimination"]
calculations = ["mean", "max"]
combinations = list(map(lambda x: '_'.join(x), product(score_types, calculations)))
scores_list = list()
for score_type, calculation in product(score_types, calculations):
    score_id = '_'.join((score_type.replace(" ", "_").replace("-", "_"), calculation))
    scores_df = df.groupby(['project', 'version', 'version_num', 'feature_selection',
        'original_num_files_per_version', 'original_num_defective_files_per_version', 'original_training_num_files',
        'original_testing_num_files', 'original_training_num_defective_files', 'original_testing_num_defective_files',
        'num_training_files', 'num_testing_files', 'num_training_defective_files', 'num_testing_defective_files',
        'defective_ratio', 'metrics_configuration']).aggregate({score_type: calculation})
    scores_df.rename(columns={score_type: score_id}, inplace=True)
    scores_list.append(scores_df)

scores = pd.concat(scores_list, axis=1).reset_index()
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores_defective", "calculated_data.csv"))
scores.to_csv(path, index=False)



