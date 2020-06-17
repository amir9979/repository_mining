import argparse
from projects import ProjectName, Project
from data_extractor import DataExtractor
from version_selector import VersionType
from config import Config
import os
from pathlib import Path
import pandas as pd
from metrics.version_metrics import Extractor
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataName

class Main():
    def __init__(self):
        self.project = None
        self.extractor = None

    def list_projects(self):
        print("\n".join(list(map(lambda e: "{0}: {1}".format(e.name, e.value.description()), ProjectName))))

    def extract(self):
        self.extractor.extract()

    def set_project(self, github, jira):
        self.project = Project(github, jira)
        self.set_extractor()

    def set_project_enum(self, name):
        self.project = ProjectName[name].value
        self.set_extractor()

    def set_extractor(self):
        self.extractor = DataExtractor(self.project)

    def organize_bin_versions(self):
        data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsBin']
        path = os.path.join(data, selected, self.project.github() + ".csv")
        in_path = Config.get_work_dir_path(path)
        versions = "versions"
        Path(versions).mkdir(parents=True, exist_ok=True)
        dest_path = os.path.join(versions, self.project.github() + ".csv")
        if os.path.exists(in_path):
            df = pd.read_csv(in_path)
            df.head(8).drop(columns=["start", "step", "stop"]).to_csv(dest_path, index=False)
        return path

    def extract_metrics(self):
        repo_data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsBin']
        path = os.path.join(repo_data, selected, self.project.github() + ".csv")
        in_path = Config.get_work_dir_path(path)
        classes_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['ClassesData'], self.project.github()))
        method_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['MethodData'], self.project.github()))
        Path(classes_data).mkdir(parents=True, exist_ok=True)
        Path(method_data).mkdir(parents=True, exist_ok=True)
        versions = pd.read_csv(in_path)['version']
        for version in versions:
            for extractor in Extractor.get_all_extractors(self.project, version):
                extractor.extract()
            db = DataBuilder(self.project, version)
            list(map(lambda d: db.append(d), DataName))
            classes_df, methods_df = db.build()
            classes_df.to_csv(os.path.join(classes_data, version + ".csv"), index=False)
            methods_df.to_csv(os.path.join(method_data, version + ".csv"), index=False)

    def main(self):
        parser = argparse.ArgumentParser(description='Execute project data')
        parser.add_argument('-p', '--projects', dest='projects', action='store_const', const=True, default=False,
                            help='list all aleready defined projects')
        parser.add_argument('-c', '--choose', dest='choose', action='store', help='choose a project to extract')
        parser.add_argument('-g', '--github_url', dest='github', action='store', help='the git link to the project to extract')
        parser.add_argument('-j', '--jira_url', dest='jira', action='store', help='the jira link to the project to extract')
        parser.add_argument('-s', '--select_verions', dest='select', action='store', help='the algorithm to select the versions : [bin]', default='bin')
        parser.add_argument('-n', '--num_verions', dest='num_versions', action='store', help='the number of versions to select', default=5, type=int)
        parser.add_argument('-t', '--versions_type', dest='versions_type', action='store', help='the versions type to select', default="Untyped")
        args = parser.parse_args()
        if args.projects:
            self.list_projects()
        if args.choose:
            self.set_project_enum(args.choose)
        if args.github and args.jira:
            self.set_project(args.github, args.jira)
        if args.select:
            self.extractor.choose_versions(version_num=args.num_versions, algorithm=args.select, strict="false", version_type=VersionType[args.versions_type])
            self.extract()
            self.extract_metrics()



if __name__ == "__main__":
    Main().main()