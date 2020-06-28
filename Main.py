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
from classification_instance import ClassificationInstance


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
        classes_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['ClassesData'], self.project.github()))
        Path(classes_data).mkdir(parents=True, exist_ok=True)
        method_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['MethodData'], self.project.github()))
        Path(method_data).mkdir(parents=True, exist_ok=True)

        classes_datasets = []
        methods_datasets = []

        for version in self.get_selected_versions():
            classes_df, methods_df = self.extract_features_to_version(classes_data, method_data, version)
            methods_datasets.append(methods_df)
            classes_datasets.append(classes_df)

        classes_instance = self.extract_classes_datasets(classes_datasets)
        classes_instance.predict()


    def extract_features_to_version(self, classes_data, method_data, version):
        for extractor in Extractor.get_all_extractors(self.project, version):
            extractor.extract()
        db = DataBuilder(self.project, version)
        list(map(lambda d: db.append(d), DataName))
        classes_df, methods_df = db.build()
        methods_df.fillna(False, inplace=True)
        methods_df.to_csv(os.path.join(method_data, version + ".csv"), index=False)

        aggregation_fns = {feature: lambda value: any(value) for feature in list(methods_df.columns)[3:]}
        aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
        classes_df.dropna(inplace=True)
        classes_df = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
        classes_df.fillna(False, inplace=True)
        classes_df.to_csv(os.path.join(classes_data, version + ".csv"), index=False)

        return classes_df, methods_df

    def extract_classes_datasets(self, classes_datasets):
        dataset_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Dataset'],
                         self.project.github()))
        classes_dataset_dir = os.path.join(dataset_dir, "classes")
        Path(classes_dataset_dir).mkdir(parents=True, exist_ok=True)
        classes_training = pd.concat(classes_datasets[:-1], ignore_index=True).drop(["File", "Class"], axis=1)
        classes_testing = classes_datasets[-1]
        classes_testing_names = classes_testing.pop(["File", "Class"])
        return ClassificationInstance(classes_training, classes_testing, classes_testing_names,
                                      os.path.join(classes_dataset_dir, "training.csv"),
                                      os.path.join(classes_dataset_dir, "testing.csv"),
                                      os.path.join(classes_dataset_dir, "prediction.csv"))

    def extract_methods_datasets(self, methods_datasets):
        dataset_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Dataset'],
                         self.project.github()))
        methods_dataset_dir = os.path.join(dataset_dir, "methods")
        Path(methods_dataset_dir).mkdir(parents=True, exist_ok=True)
        methods_training = pd.concat(methods_datasets[:-1], ignore_index=True).drop(["File", "Class"], axis=1)
        methods_testing = methods_datasets[-1]
        methods_testing_names = methods_testing.pop(["File", "Class"])
        return ClassificationInstance(methods_training, methods_testing, methods_testing_names,
                                      os.path.join(methods_dataset_dir, "training.csv"),
                                      os.path.join(methods_dataset_dir, "testing.csv"),
                                      os.path.join(methods_dataset_dir, "prediction.csv"))


    def get_selected_versions(self):
        repo_data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsBin']
        path = os.path.join(repo_data, selected, self.project.github() + ".csv")
        in_path = Config.get_work_dir_path(path)
        return pd.read_csv(in_path)['version'].to_list()


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