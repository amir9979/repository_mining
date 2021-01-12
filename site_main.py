import argparse
from projects import ProjectName, Project
from data_extractor import DataExtractor
from version_selector import VersionType
from config import Config
import os
import json
from pathlib import Path
import pandas as pd
from metrics.version_metrics import Extractor
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataNameEnum
from classification_instance import ClassificationInstance
from itertools import tee
import time
from functools import reduce
import traceback


class SiteMain():
    def __init__(self):
        self.project = None
        self.extractor = None
        self.jira_url = None
        self.github_user_name = None
        self.quick_mode = False

    def set_project(self, github_name, github_user, jira_name, jira_url):
        self.project = Project(github_name, github_user, '', [jira_name], [], jira_url, '')

    def set_project_enum(self, name):
        self.project = ProjectName[name].value

    def get_classes_data(self):
        return Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'],
                                                             Config().config['VERSION_METRICS']['ClassesData'],
                                                             self.project.github_name))

    def get_and_clean_out_dir(self, out):
        out_dir = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'],
                                                             out))
        try:
            Path(out_dir).rmdir()
        except OSError as e:
            print("Error: %s : %s" % (out_dir, e.strerror))
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        return out_dir

    def main(self):
        parser = argparse.ArgumentParser(description='Execute project data')
        parser.add_argument('-p', '--projects', dest='projects', action='store_const', const=True, default=False,
                            help='list all aleready defined projects')
        parser.add_argument('-c', '--choose', dest='choose', action='store', help='choose a project to extract')
        parser.add_argument('-g', '--github_repo_name', dest='github_repo', action='store', help='the github repository name to the project to extract (lowercase)')
        parser.add_argument('-j', '--jira_product_name', dest='jira_product', action='store', help='the jira name to the project to extract (uppercase)')
        parser.add_argument('-u', '--github_user_name', dest='github_user_name', action='store', help='the github user name to the project to extract (lowercase)', default="apache")
        parser.add_argument('-jl', '--jira_url', dest='jira_url', action='store', help='the link to jira', default="http://issues.apache.org/jira")

        parser.add_argument('-o', '--out_dir', dest='out_dir', action='store', help='', default="tmp_out")
        parser.add_argument('rest', nargs=argparse.REMAINDER)

        args = parser.parse_args()
        if args.choose:
            self.set_project_enum(args.choose)
        if args.github_repo and args.jira_product:
            self.set_project(args.github_repo, args.github_user_name, args.jira_product, args.jira_url)

        rest = args.rest
        out_dir = self.get_and_clean_out_dir(args.out_dir)
        classes_data = self.get_classes_data()
        for file_name in os.listdir(classes_data):
            if "aggregated_classes_" in file_name:
                continue
            df = pd.read_csv(os.path.join(classes_data, file_name), sep=';')
            rest_cols = [r for r in rest if r in df.columns]
            df = df[['File'] + rest_cols]
            df.to_csv(os.path.join(out_dir, file_name), sep=';')


if __name__ == "__main__":
    m = SiteMain()
    m.main()
