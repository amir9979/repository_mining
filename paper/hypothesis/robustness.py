import os
from itertools import product

from numpy import mean
from pandas import DataFrame
import pandas as pd
from plotnine import ggplot, aes, geom_bar, geom_col, ggtitle, labs, xlab, ylab, save_as_pdf_pages

from config import Config
from projects import ProjectName


class RobustnessTest:
    def __init__(self, data: DataFrame):
        self.data = data
        self.projects = data.project.unique()
        self.metrics = ['precision', 'recall', 'f1-measure', 'auc-roc', 'brier score']
        self.datasets = ['designite', 'fowler', 'designite_fowler', 'traditional',
                         'designite_traditional', 'fowler_traditional', 'designite_fowler_traditional']

    def get_average_distance(self):
        return self.get_distance_by_fn(mean)

    def get_max_distance(self):
        return self.get_distance_by_fn(max)

    def get_distance_by_fn(self, fn):
        distances = []
        for metric, dataset in product(self.metrics, self.datasets):
            distances.append(
                (metric, dataset, fn(list(map(lambda x: self.calculate_distances(x, metric, dataset), self.projects)))))
        return distances

    def calculate_distances(self, project, metric, dataset):
        if dataset == "brier score":
            fn = min
        else:
            fn = max
        best = self.calculate_best(project, metric, fn)
        cond1 = self.data['project'] == project
        cond2 = self.data['dataset'] == dataset
        i = self.data.loc[cond1 & cond2][metric].values[0]
        return best - i

    def calculate_best(self, project, metric, feature_selection, fn=max):
        """

        :param project: name of the project
        :param metric:
        :param datasets:
        :param fn: function to get the best
        :return:
        """

        cond = self.data['project'] == project
        cond2 = self.data['feature_selection'] == feature_selection
        return fn(self.data.loc[cond][metric])


projects = list(map(lambda x: x.github(), list(ProjectName)))
max_scores_rows = list()
mean_scores_rows = list()

datasets = ['designite', 'fowler',
            'designite_fowler', 'traditional',
            'designite_traditional', 'fowler_traditional',
            'designite_fowler_traditional',
            ]

fs_methods = ['chi2_20p', 'mutual_info_classif_20p', 'f_classif_20', 'recursive_elimination', 'all']
metrics = ['precision', 'recall', 'f1-measure', 'auc-roc', 'brier score']

for project in projects:
    try:
        dataset_dict = {}
        for dataset in datasets:
            path = Config.get_work_dir_path(os.path.join("paper", "analysis", dataset, project, 'scores.csv'))
            df = pd.read_csv(path)
            mean_df = df.groupby('feature_selection').aggregate({metric: 'mean' for metric in metrics}).reset_index()
            max_df = df.groupby('feature_selection').aggregate({metric: 'max' for metric in metrics}).reset_index()
            dataset_dict[dataset] = {'mean': mean_df, 'max': max_df}

            mean_scores_rows += [{'project': project,
                                  'dataset': dataset,
                                  'feature_selection': row[1][0],
                                  'precision': row[1][1],
                                  'recall': row[1][2],
                                  'f1-measure': row[1][3],
                                  'auc-roc': row[1][4],
                                  'brier score': row[1][5]
                                  } for row in mean_df.iterrows()]

            max_scores_rows += [{'project': project,
                                 'dataset': dataset,
                                 'feature_selection': row[1][0],
                                 'precision': row[1][1],
                                 'recall': row[1][2],
                                 'f1-measure': row[1][3],
                                 'auc-roc': row[1][4],
                                 'brier score': row[1][5]
                                 } for row in max_df.iterrows()]

    except Exception:
        max_scores_rows = list(filter(lambda x: x['project'] != project, max_scores_rows))
        mean_scores_rows = list(filter(lambda x: x['project'] != project, mean_scores_rows))
        continue

mean_scores_df = pd.DataFrame(mean_scores_rows)
max_scores_df = pd.DataFrame(max_scores_rows)

plots = []
for fs_method in fs_methods:
    cond = max_scores_df['feature_selection'] == fs_method
    max_t = RobustnessTest(max_scores_df.loc[cond])
    cond = mean_scores_df['feature_selection'] == fs_method
    mean_t = RobustnessTest(mean_scores_df.loc[cond])
    columns = ['Metric', 'Dataset', 'Distance']
    max_avg_dist = max_t.get_average_distance()
    max_avg_dist_df = pd.DataFrame(max_avg_dist, columns=columns)
    max_max_dist = max_t.get_max_distance()
    max_max_dist_df = pd.DataFrame(max_max_dist, columns=columns)
    mean_avg_dist = mean_t.get_average_distance()
    mean_avg_dist_df = pd.DataFrame(mean_avg_dist, columns=columns)
    mean_max_dist = mean_t.get_max_distance()
    mean_max_dist_df = pd.DataFrame(mean_max_dist, columns=columns)

    plots.append((ggplot(max_avg_dist_df, aes(x="Metric", y="Distance", fill="Dataset"))
                  + geom_bar(stat='identity', position='dodge')
                  + labs(title="Feature Selection {} | Maximum Classifier Score | Average Error Distance".format(fs_method),
                         )
                  + ylab("Average Error")
                  ))

    plots.append((ggplot(max_max_dist_df, aes(x="Metric", y="Distance", fill="Dataset"))
                  + geom_bar(stat='identity', position='dodge')
                  + labs(title="Feature Selection {} | Maximum Classifier Score | Maximum Error Distance".format(fs_method),
                         )
                  + ylab("Max Error")
                  ))

    plots.append((ggplot(mean_avg_dist_df, aes(x="Metric", y="Distance", fill="Dataset"))
                  + geom_bar(stat='identity', position='dodge')
                  + labs(title="Feature Selection {} | Average Classifier Score  | Average Error Distance".format(fs_method),
                         )
                  + ylab("Avg Error")
                  ))

    plots.append((ggplot(mean_max_dist_df, aes(x="Metric", y="Distance", fill="Dataset"))
                  + geom_bar(stat='identity', position='dodge')
                  + labs(title="Feature Selection {} | Average Classifier Score | Maximum Error Distance".format(fs_method),
                         )
                  + ylab("Max Error")
                  ))


path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "robustness.pdf"))
save_as_pdf_pages(plots, path=path)
