import os
from itertools import product

import pandas as pd
import numpy as np
from plotnine import ggplot, geom_violin, aes, geom_boxplot, geom_col, labs, save_as_pdf_pages, ggtitle, \
    scale_fill_gradient, scale_fill_manual, ylim
from scipy import stats
from sklearn.preprocessing import MinMaxScaler

from config import Config
from paper.hypothesis.hypothesis import Hypothesis
from projects import ProjectName


def get_scores(dataset1, dataset2, projects_, score):
    failed_count = 0
    output1 = []
    output2 = []
    for project_ in projects_:
        try:
            scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", dataset1, project_, "scores.csv"))
            scores_df = pd.read_csv(scores_path)
            scores_cond = scores_df['feature_selection'] == "all"
            value1 = max(scores_df.loc[scores_cond][score].values)
            scores_path = Config.get_work_dir_path(os.path.join("paper", "analysis", dataset2, project_, "scores.csv"))
            scores_df = pd.read_csv(scores_path)
            scores_cond = scores_df['feature_selection'] == "all"
            value2 = max(scores_df.loc[scores_cond][score].values)
            output1.append(value1)
            output2.append(value2)
        except Exception:
            failed_count += 1
            print("failed extracting {}".format(project_))
    print("Failed {} Projects".format(failed_count))
    return output1, output2


def get_all_hypothesis(data, project_id, bin_criteria, h0, h1, prefix, suffix, p1, p2, n_bins=5):
    """

    :param data: dataframe with info we want to extract hypothesis
    :param project_id: column name of the project name column
    :param bin_criteria: column name for the criteria to divide into bins
    :param h0: comparison for null hypothesis
    :param h1: comparison for hypothesis
    :param prefix: text before comparison of the hypothesis
    :param suffix: text after comparison of the hypothesis
    :param p1: first comparison parameter of the hypothesis
    :param p2: second comparison parameter of the hypothesis
    :param n_bins: number of bins
    :return: all hypothesis objects
    """

    labels = ["bin_" + str(i+1) for i in range(n_bins)]
    data['quantile_distribution_bins'] = pd.qcut(data[bin_criteria], q=n_bins, labels=labels)
    data['quantile_distribution_values'] = pd.qcut(data[bin_criteria], q=n_bins)
    data['constant_distribution_bins'] = pd.cut(data[bin_criteria], bins=n_bins, labels=labels)
    data['constant_distribution_values'] = pd.cut(data[bin_criteria], bins=n_bins)

    bin_types = ['quantile', 'constant']
    metrics = ['f1-measure', 'auc-roc', 'brier score']
    hypothesis = {bin_type: {metric: list() for metric in metrics} for bin_type in bin_types}
    for metric, bin_type, label in product(metrics, bin_types, labels):
        distribution_bin = "{}_distribution_bins".format(bin_type)
        distribution_values = "{}_distribution_values".format(bin_type)
        cond = data[distribution_bin] == label
        project_names = data.loc[cond][project_id]
        bin_range = projects_info.loc[cond][distribution_values].values[0]
        formatted_suffix = suffix.format(metric, bin_range, label, bin_type)
        data1, data2 = get_scores("designite_fowler", "fowler", project_names, metric)
        h = Hypothesis(h0=h0, h1=h1, prefix=prefix, suffix=formatted_suffix, p1=p1, p2=p2, data1=data1, data2=data2)
        print(h)
        hypothesis[bin_type][metric].append({label: h})
    return hypothesis


def plot_hypothesis(hypothesis, file_name):
    bin_types = list(hypothesis)
    scores = list(hypothesis[bin_types[0]])
    plots = []
    for bin_type, score in product(bin_types, scores):
        mean_name = "Mean: " + score
        df = pd.DataFrame(columns=["Bin", "Dataset", mean_name])
        df2 = pd.DataFrame(columns=["Bin", "t-statistic", 'p-value'])
        for bin_ in hypothesis[bin_type][score]:
            h = list(bin_.values())[0]
            bin_name = list(bin_)[0]
            parameter1 = h.p1
            parameter2 = h.p2
            mean1 = h.mean1
            mean2 = h.mean2
            row1 = {"Bin": bin_name, 'Dataset': parameter1, mean_name: str(round(float(mean1), 3))}
            row2 = {"Bin": bin_name, 'Dataset': parameter2, mean_name: str(round(float(mean2), 3))}
            df = df.append(row1, ignore_index=True)
            df = df.append(row2, ignore_index=True)
            t_statistic = h.t
            p_value = h.p
            row = {"Bin": bin_name, 't-statistic': str(round(t_statistic, 3)), 'p-value': str(p_value), '95% Confidence': "Significant" if p_value <= 0.05 else "Not Significant"}
            df2 = df2.append(row, ignore_index=True)
        plots.append((ggplot(df, aes(x='Bin', y=mean_name, fill='Dataset'))
                      + geom_col(stat='identity', position='dodge')
                      + ggtitle("{0} bin distribution| {1}\nBin's Average Scores".format(bin_type, score))))
        plots.append((ggplot(df2, aes(x='Bin', y='p-value', fill='95% Confidence'))
                      + geom_col(stat='identity', width=0.2)
                      + ggtitle("{0} bin distribution| {1}\nBin's 95% Confidence Level Test".format(bin_type, score))
                      + scale_fill_manual(values={'Significant': "#214517", 'Not Significant': '#c62f2d'})))
    save_as_pdf_pages(plots, file_name)

    return
'''
    - Numerical Data
    - Two Samples: projects with large scale & projects with small scale
    - Two Sample T-Test
'''


'''
    H0: Models trained with designite and fowler smells combined produce lower or equal f1-scores for projects of larger scale than
    lower scale, ie. projects with more than 50 people and with more than 6 months.

    H1: Models trained with designite and fowler smells combined produce higher f1-scores for projects of larger scale than
    lower scale, ie. projects with more than 50 people and with more than 6 months.
'''


path = Config.get_work_dir_path(os.path.join("paper", "graphics", "projects", "projects_info.csv"))
projects_info = pd.read_csv(path)
NUM_CONTRIBUTORS_WEIGHT = 0.5
DURATION_WEIGHT = 0.5
BINS = 5

scores = list(map(lambda x, y:
                  DURATION_WEIGHT * x + NUM_CONTRIBUTORS_WEIGHT * y,
                  list(MinMaxScaler().fit_transform(np.vstack(np.array(projects_info.duration_days)))),
                  list(MinMaxScaler().fit_transform(np.vstack(np.array(projects_info.num_contributors))))))

projects_info['score'] = np.array(scores).flatten()
h0 = "lower or equal"
h1 = "higher"
prefix = "Models trained with designite and fowler smells combined produce for projects with scores"
suffix = "{0} than models trained with only fowler smells, for projects with score between {1} => {2} | {3} distribution bin."
p1 = "Designite + Fowler"
p2 = "Fowler"
hypothesis = get_all_hypothesis(data=projects_info, project_id='project', bin_criteria='score', h0=h0, h1=h1, prefix=prefix, suffix=suffix, p1=p1, p2=p2)
path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "1st_parameter__num_contributers_and_duration.pdf"))
plot_hypothesis(hypothesis, path)

path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "1st_parameter_num_contributers.csv"))
projects_info.to_csv(path)

'''
    H0: Models trained with designite and fowler smells combined produce lower or equal f1-scores for projects of larger scale than
    lower scale, ie. projects with more than 5000 training and testing instances.

    H1: Models trained with designite and fowler smells combined produce higher f1-scores for projects of larger scale than
    lower scale, ie. projects with more than 5000 training and testing instances.
'''

projects = list(map(lambda x: x.github(), list(ProjectName)))
projects_sizes = list()
for index, project in enumerate(projects):
    try:
        training_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "training.csv"))
        testing_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "testing.csv"))

        size = len(pd.read_csv(training_path)) + len(pd.read_csv(testing_path))
        projects_sizes.append(size)
    except Exception:
        del projects[index]
        print("Failed project {}".format(project))
        continue

projects_sizes_df = pd.DataFrame({'project': projects, 'size': projects_sizes})
h0 = "lower or equal"
h1 = "higher"
prefix = "Models trained with designite and fowler smells combined produce for projects with scores"
suffix = "{0} than models trained with only fowler smells, for projects with number of instances between {1} => {2} | {3} distribution bin."
p1 = "Designite + Fowler"
p2 = "Fowler"
hypothesis = get_all_hypothesis(data=projects_sizes_df, project_id="project", bin_criteria="size", h0=h0, h1=h1, prefix=prefix, suffix=suffix, p1=p1, p2=p2)
path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "2st_parameter__num_instances.pdf"))
plot_hypothesis(hypothesis, path)

path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "2st_parameter_num_instances.csv"))
projects_sizes_df.to_csv(path, index=False)

'''
    3rd parameter: Number of Bugs
'''

projects = list(map(lambda x: x.github(), list(ProjectName)))
projects_num_defects = list()
for index, project in enumerate(projects):
    try:
        training_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "training.csv"))
        testing_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "testing.csv"))

        training_df = pd.read_csv(training_path)
        testing_df = pd.read_csv(testing_path)
        cond = training_df['Bugged']
        num_training_defects = len(training_df.loc[cond])
        cond = testing_df['Bugged']
        num_testing_defects = len(testing_df.loc[cond])
        num_defects = num_training_defects + num_testing_defects
        projects_num_defects.append(num_defects)
    except Exception:
        del projects[index]
        print("Failed project {}".format(project))
        continue

projects_num_defects_df = pd.DataFrame({'project': projects, 'num_defects': projects_num_defects})
h0 = "lower or equal"
h1 = "higher"
prefix = "Models trained with designite and fowler smells combined produce for projects with scores"
suffix = "{0} than models trained with only fowler smells, for projects with number of defects between {1} => {2} | {3} distribution bin."
p1 = "Designite + Fowler"
p2 = "Fowler"
hypothesis = get_all_hypothesis(data=projects_num_defects_df, project_id="project", bin_criteria="num_defects", h0=h0, h1=h1, prefix=prefix, suffix=suffix, p1=p1, p2=p2)
path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "3st_parameter__num_bugs.pdf"))
plot_hypothesis(hypothesis, path)

path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "3st_parameter_num_bugs.csv"))
projects_num_defects_df.to_csv(path)

'''
    - Numerical Data
    - Two Samples: projects with defect ratio higher than 10% & lower than 10%
    - Two Sample T-Test
'''

'''
    H0: Models trained with designite and fowler smells combined, produce lower f1-scores for projects with a defect ratio
    higher than 10%.

    H1: Models trained with designite and fowler smells combined, produce higher f1-scores for projects with a defect ratio
    higher than 10%.
'''

projects = list(map(lambda x: x.github(), list(ProjectName)))
projects_ratios = list()
for index, project in enumerate(projects):
    try:
        training_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "training.csv"))
        testing_path = Config.get_work_dir_path(
            os.path.join("paper", "analysis", "designite_fowler", project, "dataset", "testing.csv"))


        training_df = pd.read_csv(training_path)
        testing_df = pd.read_csv(testing_path)
        size = len(training_df) + len(testing_df)
        training_cond = training_df['Bugged']
        testing_cond = testing_df['Bugged']
        bugged = len(training_df.loc[training_cond]) + len(testing_df.loc[testing_cond])
        ratio = (bugged / size) * 100
        projects_ratios.append(ratio)

    except Exception:
        del projects_ratios[index]
        print("Failed project {}".format(project))
        continue

projects_ratios_df = pd.DataFrame({'project': projects, 'ratio': projects_ratios})
h0 = "lower or equal"
h1 = "higher"
prefix = "Models trained with designite and fowler smells combined produce for projects with scores"
suffix = "{0} than models trained with only fowler smells, for projects with the ratios between {1} => {2} | {3} distribution bin."
p1 = "Designite + Fowler"
p2 = "Fowler"
hypothesis = get_all_hypothesis(data=projects_ratios_df, project_id="project", bin_criteria="ratio", h0=h0, h1=h1, prefix=prefix, suffix=suffix, p1=p1, p2=p2)
path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "4st_parameter__ratios.pdf"))
plot_hypothesis(hypothesis, path)

path = Config.get_work_dir_path(os.path.join("paper", "hypothesis", "4st_parameter_ratios.csv"))
projects_ratios_df.to_csv(path)
