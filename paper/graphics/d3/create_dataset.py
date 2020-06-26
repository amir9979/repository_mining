import os

import pandas as pd

from config import Config
from projects import ProjectName

projects = list(map(lambda x: x.github(), list(ProjectName)))
working_projects = dict()
for project in projects:
    try:
        designite_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "designite", project, "scores.csv"))
        designite_scores_df = pd.read_csv(designite_scores_path)
        designite_scores_df['dataset'] = 'Designite'
        designite_scores_df['project'] = project

        fowler_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "fowler", project, "scores.csv"))
        fowler_scores_df = pd.read_csv(fowler_scores_path)
        fowler_scores_df['dataset'] = 'Fowler'
        fowler_scores_df['project'] = project

        # traditional_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "traditional", project, "scores.csv"))
        # traditional_scores_df = pd.read_csv(traditional_scores_path)
        # traditional_scores_df['dataset'] = 'Traditional'
        # traditional_scores_df['project'] = project

        traditional_fowler_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "fowler_traditional", project, "scores.csv"))
        traditional_fowler_scores_df  = pd.read_csv(traditional_fowler_scores_path)
        traditional_fowler_scores_df['dataset'] = 'Traditional +\n Fowler'
        traditional_fowler_scores_df['project'] = project

        # traditional_designite_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "traditional_designite", project, "scores.csv"))
        # traditional_designite_scores_df = pd.read_csv(traditional_designite_scores_path)
        # traditional_designite_scores_df['dataset'] = 'Traditional +\n Designite'
        # traditional_designite_scores_df['project'] = project

        designite_fowler_scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "designite_fowler", project, "scores.csv"))
        designite_fowler_scores_df = pd.read_csv(designite_fowler_scores_path )
        designite_fowler_scores_df['dataset'] = 'Designite +\n Fowler'
        designite_fowler_scores_df['project'] = project

        traditional_designite_fowler_path = Config.get_work_dir_path(os.path.join("paper", "analysis", "designite_fowler_traditional", project, "scores.csv"))
        traditional_designite_fowler_scores_df  = pd.read_csv(traditional_designite_fowler_path)
        traditional_designite_fowler_scores_df['dataset'] = 'Traditional +\n Designite +\n Fowler'
        traditional_designite_fowler_scores_df['project'] = project

        datasets = [
            designite_scores_df,
            fowler_scores_df,
            # traditional_scores_df,
            traditional_fowler_scores_df,
            # traditional_designite_scores_df,
            designite_fowler_scores_df,
            traditional_designite_fowler_scores_df
        ]

        scores_df = pd.concat(datasets, ignore_index=True)
        working_projects[project] = scores_df
    except Exception:
        continue

