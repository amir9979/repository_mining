import os

import pandas as pd
from plotnine import ggplot, aes, geom_col, ggtitle, scale_fill_manual, save_as_pdf_pages

from config import Config
from paper.hypothesis.hypothesis import Hypothesis

'''
    - Numerical Data
    - Two Samples: Designite + Fowler & Fowler
    - Two Sample T-Test
'''

'''
    H0: Models trained with designite and fowler smells combined produce lower or equal f1-scores than models trained with only
    fowler smells.

    H1: Models trained with designite and fowler smells combined produce higher f1-scores than models trained with only
    fowler smells.
'''
scores = [
    "precision_mean", "precision_max",
    "recall_mean", "recall_max",
    "f1_measure_mean", "f1_measure_max",
    "auc_roc_mean", "auc_roc_max",
    "brier_score_mean", "brier_score_max"]

plots = []

for score in scores:
    path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores", "data.csv"))
    df = pd.read_csv(path, sep=';')

    cond = df['dataset'] == "Designite + Fowler"
    designite_fowler = df.loc[cond][score]
    cond = df['dataset'] == 'Fowler'
    fowler = df.loc[cond][score]

    h0 = "lower or equal"
    h1 = "higher"
    prefix = "Models trained with designite and fowler smells combined produce"
    suffix = "{} than models trained with only fowler smells, if we take the maximum of classifiers.".format(score)
    p1 = "Designite + Fowler"
    p2 = "Fowler"
    data1 = designite_fowler
    data2 = fowler

    h = Hypothesis(h0=h0, h1=h1, prefix=prefix, suffix=suffix, p1=p1, p2=p2, data1=data1, data2=data2)
    print(h)

