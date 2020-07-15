'''
    project name
    age
    number contributors
    number files
    {v1...v5}
    number defects
    {v1...v5}

Project | Age (months) | Number Contributors |      Number Files      |      Number Defects
                                             | v1 | v2 | v3 | v4 | v5 | v1 | v2 | v3 | v4 | v5

+ use multindex to handle versions
https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html
'''
from projects import ProjectName

'''
    # special note
    if we consider only fowler <-> designite relation => then we are able to consider 97 projects
'''

import os
from itertools import product

import pandas as pd

from config import Config

path = Config.get_work_dir_path(os.path.join("paper", "graphics", "projects", "projects_info.csv"))
info_df = pd.read_csv(path)

# metrics = ["designite", "designite_fowler", "designite_fowler_traditional", "designite_traditional", "fowler", "fowler_traditional", "traditional"]
metrics = ["designite", "designite_fowler", "fowler"]

exclusion = set()
for project, metric in product(info_df['project'].values, metrics):
    score_path = Config.get_work_dir_path(os.path.join("paper", "analysis", metric, project, "scores.csv"))
    if not os.path.exists(score_path):
        exclusion.add(project)
        continue


def split1(data):
    return data[:int(round(len(data) / 2))]


def split2(data):
    return data[int(round(len(data) / 2)):]


def flatten(data):
    return [item for sublist in data for item in sublist]


def transpose(data):
    return [flatten(list(map(list, zip(*row)))) for row in data]


projects = list(filter(lambda x: x not in exclusion, info_df['project'].values))
duration = list(map(lambda x: int(round(x / 30)), list(info_df[info_df['project'].isin(projects)]['duration_days'])))
num_contributors = list(info_df.loc[info_df['project'].isin(projects)]['num_contributors'])

projects_1 = split1(projects)
duration_1 = split1(duration)
num_contributors_1 = split1(num_contributors)

projects_2 = split2(projects)
duration_2 = split2(duration)
num_contributors_2 = split2(num_contributors)

index_1 = pd.MultiIndex.from_arrays([projects_1, duration_1, num_contributors_1],
                                    names=['Project', 'Age(Mth)', '#Cntrb'])
columns_1 = pd.MultiIndex.from_product([['#Files', '#Defects', '%Defects'], ['v1', 'v2', 'v3', 'v4', 'v5']],
                                       names=['', 'Versions'])
index_2 = pd.MultiIndex.from_arrays([projects_2, duration_2, num_contributors_2],
                                    names=['Project', 'Age(Mth)', '#Cntrb'])
columns_2 = pd.MultiIndex.from_product([['#Files', '#Defects', '%Defects'], ['v1', 'v2', 'v3', 'v4', 'v5']],
                                       names=['', 'Versions'])

data = []

jira_dict = {project.github(): project.jira() for project in list(ProjectName)}
for project in projects:
    versions_path = Config.get_work_dir_path(os.path.join("paper", "versions", project + ".csv"))
    versions = pd.read_csv(versions_path)['version'].values
    versions_info_path = Config.get_work_dir_path(os.path.join("repository_data",
                                                               "apache_versions",
                                                               project,
                                                               "{}.csv".format(jira_dict[project])))
    versions_info_df = pd.read_csv(versions_info_path)
    data.append([(versions_info_df.loc[versions_info_df['version_name'] == version][
                      '#commited_files_in_version'].values[0],
                  versions_info_df.loc[versions_info_df['version_name'] == version]['#bugged_files_in_version'].values[
                      0],
                  str(round(float(
                      versions_info_df.loc[versions_info_df['version_name'] == version]['bugged_ratio'].values[
                          0]) * 100, 1)),
                  ) for version in versions])

data1 = transpose(split1(data))
data2 = transpose(split2(data))
pd.DataFrame(data1, columns=columns_1, index=index_1).to_latex("table1.tex")
print(pd.DataFrame(data1, columns=columns_1, index=index_1))
pd.DataFrame(data2, columns=columns_2, index=index_2).to_latex("table2.tex")
