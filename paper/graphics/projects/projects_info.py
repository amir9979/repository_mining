import os

import requests

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from config import Config
from projects import ProjectName

projects = list(ProjectName)

columns = ['project', 'start_date', 'end_date', 'duration_days', 'duration_delta', 'num_contributors']
projects_info_dicts = []
for project in tqdm(projects, total=len(projects)):
    try:
        r = requests.get("https://github.com/apache/{}".format(project.github()))
        soup = BeautifulSoup(r.text, features="lxml")
        number_contributors = soup.find("a", {"href": "/apache/{}/graphs/contributors".format(project.github())}).contents[1].contents[0]
    except Exception:
        number_contributors = "nan"

    repo_data = Config.get_work_dir_path(Config().config['CACHING']['RepositoryData'])
    versions_path = os.path.join(repo_data, "apache_versions", project.github(), "{}.csv".format(project.jira()))
    versions_df = pd.read_csv(versions_path)
    start_date = min(pd.to_datetime(versions_df['version_date']))
    end_date = max(pd.to_datetime(versions_df['version_date']))


    projects_info_dicts.append({
        'project': project.github(),
        'start_date': str(start_date),
        'end_date': str(end_date),
        'duration_days': str((end_date - start_date).days),
        'duration_delta': str((end_date - start_date).delta),
        'num_contributors': number_contributors
    })

df = pd.DataFrame(projects_info_dicts, columns=columns)
path = Config.get_work_dir_path(os.path.join("paper", "graphics", "projects", "projects_info.csv"))
df.to_csv(path, index=False, sep=';')

