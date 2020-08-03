import os
from itertools import product

import pandas as pd
from tqdm import tqdm

from config import Config
from projects import ProjectName


path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores_defective", "calculated_data.csv"))
df = pd.read_csv(path, sep=';')

scores_df = df.groupby(['project',
                        'feature_selection',
                        'metrics_configuration',
                        'precision_mean', 'precision_max', 'recall_mean', 'recall_max', 'f1_measure_mean', 'f1_measure_max',
                        'auc_roc_mean', 'auc_roc_max', 'brier_score_mean', 'brier_score_max'])\
              .aggregate({
                        'original_num_files_per_version': 'sum',
                        'original_num_defective_files_per_version': 'sum',
                        'original_training_num_files': 'sum',
                        'original_testing_num_files': 'sum',
                        'original_training_num_defective_files': 'sum',
                        'original_testing_num_defective_files': 'sum',
                        'num_training_files': 'sum',
                        'num_testing_files': 'sum',
                        'num_training_defective_files': 'sum',
                        'num_testing_defective_files': 'sum'
                        })\
              .reset_index()
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores_defective", "sum_data.csv"))
scores_df.to_csv(path, index=False, sep=';')



