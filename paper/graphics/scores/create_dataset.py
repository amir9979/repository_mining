import os
from itertools import product

import pandas as pd

from config import Config
from projects import ProjectName

to_delete =["plc4x",
"tomcat",
"directory-kerby",
"cocoon",
"clerezza",
"pulsar",
"isis",
"deltaspike",
"tez",
"directory-studio",
"commons-math",
"uima-ruta",
"myfaces-tobago",
"reef",
"asterixdb",
"giraph",
"tinkerpop",
"shiro",
"commons-vfs",
"karaf",
"cxf",
"myfaces",
"directory-server",
"flink",
"servicecomb-java-chassis",
"cayenne",
"cassandra",
"olingo-odata4",
"santuario-java",
"camel",
"jackrabbit",
"nifi",
"opennlp",
"wicket",
"commons-cli"]

projects = list(map(lambda x: x.github(), list(ProjectName)))
# projects = [x for x in projects if x not in to_delete]
working_projects = dict()
worked = []
for project in projects:

    try:
        designite_scores_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite", project, "scores.csv"))
        designite_scores_df = pd.read_csv(designite_scores_path)
        designite_scores_df['dataset'] = 'Designite'
        designite_scores_df['project'] = project

        fowler_scores_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "fowler", project, "scores.csv"))
        fowler_scores_df = pd.read_csv(fowler_scores_path)
        fowler_scores_df['dataset'] = 'Fowler'
        fowler_scores_df['project'] = project

        traditional_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "traditional", project, "scores.csv"))
        traditional_scores_df = pd.read_csv(traditional_scores_path)
        traditional_scores_df['dataset'] = 'Traditional'
        traditional_scores_df['project'] = project

        traditional_fowler_scores_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "fowler_traditional", project, "scores.csv"))
        traditional_fowler_scores_df = pd.read_csv(traditional_fowler_scores_path)
        traditional_fowler_scores_df['dataset'] = 'Traditional + Fowler'
        traditional_fowler_scores_df['project'] = project

        traditional_designite_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "designite_traditional", project, "scores.csv"))
        traditional_designite_scores_df = pd.read_csv(traditional_designite_scores_path)
        traditional_designite_scores_df['dataset'] = 'Traditional + Designite'
        traditional_designite_scores_df['project'] = project

        designite_fowler_scores_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "scores.csv"))
        designite_fowler_scores_df = pd.read_csv(designite_fowler_scores_path)
        designite_fowler_scores_df['dataset'] = 'Designite + Fowler'
        designite_fowler_scores_df['project'] = project

        traditional_designite_fowler_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler_traditional", project, "scores.csv"))
        traditional_designite_fowler_scores_df = pd.read_csv(traditional_designite_fowler_path)
        traditional_designite_fowler_scores_df['dataset'] = 'Traditional + Designite + Fowler'
        traditional_designite_fowler_scores_df['project'] = project

        datasets = [
            designite_scores_df,
            fowler_scores_df,
            traditional_scores_df,
            traditional_fowler_scores_df,
            traditional_designite_scores_df,
            designite_fowler_scores_df,
            traditional_designite_fowler_scores_df
        ]

        scores_df = pd.concat(datasets, ignore_index=True)
        working_projects[project] = scores_df
        worked += [project]
    except Exception as e:
        print("failed " + project)
        continue

print(len(worked))
print(worked)
score_types = ["precision", "recall", "f1-measure", "auc-roc", "brier score"]
features_methods = ["all", "chi2_20p", "chi2_50p", "f_classif_20", "f_classif_50", "mutual_info_classif_20p",
                    "mutual_info_classif_50p", "recursive_elimination", "mutual_info_classif_50p",
                    "recursive_elimination"]
calculations = ["mean", "max"]
combinations = list(map(lambda x: '_'.join(x), product(score_types, calculations)))
scores_list = list()
for score_type, calculation in product(score_types, calculations):
    score_id = '_'.join((score_type.replace(" ", "_").replace("-", "_"), calculation))
    scores_df = pd.concat(list(map(lambda x: x.groupby(['dataset', 'feature_selection'])
                                   .aggregate({score_type: calculation})
                                   , working_projects.values())))
    scores_df.rename(columns={score_type: score_id}, inplace=True)
    scores_list.append(scores_df)

scores = pd.concat(scores_list, axis=1).reset_index()
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores", "data.csv"))
scores.to_csv(path, index=False)
