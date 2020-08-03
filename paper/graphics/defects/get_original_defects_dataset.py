import os

import pandas as pd

from config import Config
from projects import ProjectName

not_included = [
    ProjectName.ActiveMQArtemis,
    ProjectName.Airavata,
    ProjectName.Clerezza,
    ProjectName.DirectoryKerby,
    ProjectName.Flink,
    ProjectName.JClouds,
    ProjectName.Jena,
    ProjectName.Juneau,
    ProjectName.Lucene,
    ProjectName.ManifoldCF,
    ProjectName.Ofbiz,
    ProjectName.Phoenix,
    ProjectName.Plc4x,
    ProjectName.Ranger,
    ProjectName.Storm,
    ProjectName.SystemML,
    ProjectName.Tomcat,
    ProjectName.Tomee
]

projects = list(filter(lambda x: x not in not_included, list(ProjectName)))

columns = [
    'project',
    'version_number',
    'version',
    'purpose',
    'number_files',
    'number_defects'
]
data = pd.DataFrame(columns=columns)
for project in projects:
    versions_path = Config.get_work_dir_path(os.path.join("paper", "versions", project.github() + ".csv"))
    versions_df = pd.read_csv(versions_path)
    versions = list(map(lambda x: x[0], versions_df.values))
    repository_path = Config().config["CACHING"]["RepositoryData"]
    path = Config.get_work_dir_path(os.path.join(
        repository_path, "apache_versions", project.github(), project.jira() + ".csv"))
    versions_info_df = pd.read_csv(path, sep=';')
    cond = versions_info_df.version_name.isin(versions)
    versions_info_df = versions_info_df[cond].reset_index().drop('index', axis=1)
    numbers = 0
    rows = list(map(lambda x: {'project': project.github(), 'version': x[1]['version_name'], 'purpose': 'training',
                               'number_files': x[1]['#commited_files_in_version'], 'version_number': str(x[0]),
                               'number_defects': x[1]['#bugged_files_in_version']}, versions_info_df.iterrows()))
    rows[-1]['purpose'] = 'testing'
    data = data.append(rows, ignore_index=True)

path = Config.get_work_dir_path(os.path.join("paper", "graphics", "defects", "original_defects.csv"))
data.to_csv(path, index=False)
