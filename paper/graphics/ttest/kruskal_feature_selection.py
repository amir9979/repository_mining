import os
from itertools import product

import pandas as pd
from scipy.stats import ttest_ind, kruskal

from config import Config

path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores", "data.csv"))
data = pd.read_csv(path)

columns = [
    'Feature Selection',
    'Score',
    'Dataset 1',
    'Dataset 2',
    't-statistic',
    'p-value'
]

datasets = [
    "Designite",
    "Designite + Fowler",
    "Fowler",
    "Traditional",
    "Traditional + Designite",
    "Traditional + Designite + Fowler",
    "Traditional + Fowler"]

feature_selection = [
    "all",
    "chi2_20p",
    "chi2_50p",
    "f_classif_20",
    "f_classif_50",
    "mutual_info_classif_20p",
    "mutual_info_classif_50p",
    "recursive_elimination"
]

score = [
    "precision_mean",
    "precision_max",
    "recall_mean",
    "recall_max",
    "f1_measure_mean",
    "f1_measure_max",
    "auc_roc_mean",
    "auc_roc_max",
    "brier_score_mean",
    "brier_score_max"
]

ttests_dicts = []
for row in product(datasets, score):
    ds, s = row
    cond_ds = data['dataset'] == ds

    t_statistics, p_value = kruskal(
        *tuple(data.loc[cond_ds & (data['feature_selection'] == fs)][s] for fs in feature_selection))

    ttests_dict = {
        'Dataset': ds,
        'Score': s,
        't-statistics': t_statistics,
        'p-value': p_value
    }
    ttests_dicts.append(ttests_dict)

df = pd.DataFrame(ttests_dicts)
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "ttest", "kruskal_feature_selection.csv"))
df.to_csv(path, index=False, sep=';')





