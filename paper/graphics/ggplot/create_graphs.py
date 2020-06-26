import os
from plotnine import ggplot, aes, geom_boxplot, labs, theme, element_text, facet_wrap, facet_grid, geom_violin, ggtitle
from plotnine.themes.elements import Margin

from config import Config
import pandas as pd
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

score_types = ["precision", "recall", "f1-measure", "auc-roc", "brier score"]
features_methods = ["all", "chi2_20p", "chi2_50p", "f_classif_20", "f_classif_50", "mutual_info_classif_20p", "mutual_info_classif_50p", "recursive_elimination", "mutual_info_classif_50p", "recursive_elimination"]
calculations = ["mean", "max"]

for score_type in score_types:
    for features_method in features_methods:
        for calculation in calculations:
            scores_df = pd.concat(list(map(lambda x: x.drop(['estimator', 'configuration'], axis=1)
                                .groupby(['dataset', 'feature_selection'])
                                .aggregate({score_type: calculation})
                                .reset_index(), working_projects.values())))
            scores = scores_df.loc[scores_df['feature_selection'] == features_method]

            g = (ggplot(scores,
                        aes(x='dataset',
                            y=score_type))
                 + geom_violin()
                 + geom_boxplot(width=0.2)
                 + labs(title="{0} Score with features from {1}".format(score_type.capitalize(), features_method.capitalize()),
                        x="Score Measure: {}".format(score_type.capitalize()),
                        y="Feature Selection Method: {}".format(features_method.capitalize()))
                 + theme(
                        plot_title=element_text(size=30, lineheight=.8, vjust=1,
                                                family="Fira Code", face="bold", margin={'b': 25}),
                        axis_text_x=element_text(size=15, family="Fira Code"),
                        axis_text_y=element_text(size=15, family="Fira Code"),
                        axis_title_x=element_text(size=20, family="Fira Code"),
                        axis_title_y=element_text(size=20, family="Fira Code")
                    )
                 )
            pdf_dir = Config.get_work_dir_path(os.path.join("paper", "graphics", "images", "pdf"))
            png_dir = Config.get_work_dir_path(os.path.join("paper", "graphics", "images", "png"))
            csv_dir = Config.get_work_dir_path(os.path.join("paper", "graphics", "images", "csv"))
            Config.assert_dir_exists(pdf_dir)
            Config.assert_dir_exists(png_dir)
            Config.assert_dir_exists(csv_dir)
            formatted_score_type = score_type.replace(" ", "_")
            formatted_score_type = formatted_score_type.replace(" ", "_")
            pdf_path = os.path.join(pdf_dir, "{0}_{1}_{2}".format(formatted_score_type, features_method, calculation))
            png_path = os.path.join(png_dir, "{0}_{1}_{2}".format(formatted_score_type, features_method, calculation))
            csv_path = os.path.join(csv_dir, "{0}_{1}_{2}".format(formatted_score_type, features_method, calculation))
            g.save(pdf_path, width=50, height=28.12, units="cm")
            g.save(png_path, width=50, height=28.12, units="cm")
            scores_df.to_csv(csv_path, index=False)
