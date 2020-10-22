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

class Main():
    def __init__(self):
        self.project = None
        self.extractor = None
        self.save_data_names()
        self.jira_url = None
        self.github_user_name = None

    def list_projects(self):
        print("\n".join(list(map(lambda e: "{0}: {1}".format(e.name, e.value.description()), ProjectName))))

    def extract(self):
        self.extractor.extract(True)

    def set_project(self, github, jira):
        self.project = Project(github.lower(), jira.upper())
        self.set_extractor()

    def set_project_enum(self, name):
        self.project = ProjectName[name].value
        self.set_extractor()

    def set_extractor(self):
        self.extractor = DataExtractor(self.project, self.jira_url, self.github_user_name)

    def extract_metrics(self):
        classes_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['ClassesData'], self.project.github()))
        Path(classes_data).mkdir(parents=True, exist_ok=True)
        method_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['MethodData'], self.project.github()))
        Path(method_data).mkdir(parents=True, exist_ok=True)

        classes_datasets = []
        methods_datasets = []

        for version in self.extractor.get_selected_versions()[:-1]:
            self.extractor.checkout_version(version)
            classes_df, methods_df = self.extract_features_to_version(classes_data, method_data, version)
            classes_datasets.append(classes_df)
            methods_datasets.append(methods_df)

        classes_instance = self.extract_classes_datasets(classes_datasets)
        classes_instance.predict()

        methods_instance  = self.extract_methods_datasets(methods_datasets)
        methods_instance.predict()

    def aggrate_methods_df(self, df):
        def clean(s):
            if "@" in s:
                return s[1].split('@')[1].split('.')[:-1][-1]
            return s[1].split('.')[:-1][-1]
        ids = df['Method_ids'].iteritems()
        files_id, classes_id = tee(ids, 2)
        files = pd.Series(list(map(lambda x: x[1].split('@')[0], files_id))).values
        classes = pd.Series(list(map(clean, classes_id))).values
        df.insert(0, 'File', files)
        df.insert(0, 'Class', classes)
        groupby = ['File', 'Class']
        columns_filter = ['File', 'Class', 'BuggedMethods', 'Method', 'Method_ids']
        columns = list(
            filter(lambda x: x not in columns_filter, df.columns.values.tolist()))
        data = list()
        for key, group in df.groupby(groupby):
            key_data = {}
            key_data.update(dict(zip(groupby, key)))
            for feature in columns:
                pt = pd.DataFrame(group[feature].describe()).T
                cols = ["{0}_{1}".format(feature, c) for c in pt.columns.values.tolist()]
                pt.columns = cols
                key_data.update(list(pt.iterrows())[0][1].to_dict())
            data.append(key_data)
        return pd.DataFrame(data)

    def fillna(self, df, default=False):
        if 'Bugged' in df:
            df = df[df['Bugged'].notna()]
        if 'BuggedMethods' in df :
            df = df[df['BuggedMethods'].notna()]
        for col in df:
            dt = df[col].dtype
            if dt == int or dt == float:
                df[col].fillna(0, inplace=True)
            else:
                df[col].fillna(default, inplace=True)
        return df

    def extract_features_to_version(self, classes_data, method_data, version):
        extractors = Extractor.get_all_extractors(self.project, version)
        for extractor in extractors:
            start = time.time()
            extractor.extract()
            print(time.time() - start, extractor.__class__.__name__)
        db = DataBuilder(self.project, version)
        list(map(lambda d: db.append(d), DataNameEnum))
        classes_df, methods_df = db.build()
        intermediate_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Intermediate'],
                         self.project.github()))
        classes_intermediate_dir = os.path.join(intermediate_dir, "classes")
        methods_intermediate_dir = os.path.join(intermediate_dir, "methods")
        Path(classes_intermediate_dir).mkdir(parents=True, exist_ok=True)
        Path(methods_intermediate_dir).mkdir(parents=True, exist_ok=True)
        classes_df.to_csv(os.path.join(classes_intermediate_dir, version + ".csv"), index=False, sep=';')
        methods_df.to_csv(os.path.join(methods_intermediate_dir, version + ".csv"), index=False, sep=';')

        methods_df = self.fillna(methods_df)
        aggregated_methods_df = self.aggrate_methods_df(methods_df)

        classes_df = self.fillna(classes_df)
        
        aggregated_methods_df.to_csv(os.path.join(intermediate_dir, version + "aggregated_methods_df.csv"), index=False, sep=';')
        classes_df.to_csv(os.path.join(intermediate_dir, version + "classes_df.csv"), index=False, sep=';')

        if 'Class' in classes_df.columns and 'Class' in aggregated_methods_df.columns:
            classes_df = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
        else:
            classes_df = classes_df.merge(aggregated_methods_df, on=['File'], how='outer')

        classes_df.to_csv(os.path.join(intermediate_dir, version + "merged.csv"), index=False, sep=';')

        
        classes_df = self.fillna(classes_df)
        classes_df.to_csv(os.path.join(classes_data, version + ".csv"), index=False, sep=';')

        methods_df = methods_df.drop('File', axis=1, errors='ignore')
        methods_df = methods_df.drop('Class', axis=1, errors='ignore')
        methods_df = methods_df.drop('Method', axis=1, errors='ignore')
        methods_df.to_csv(os.path.join(method_data, version + ".csv"), index=False, sep=';')

        return classes_df, methods_df

    def extract_classes_datasets(self, classes_datasets):
        dataset_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Dataset'],
                         self.project.github()))
        classes_dataset_dir = os.path.join(dataset_dir, "classes")
        Path(classes_dataset_dir).mkdir(parents=True, exist_ok=True)

        classes_training = pd.concat(classes_datasets[:-1], ignore_index=True).drop(["File", "Class", "Method_ids"], axis=1, errors='ignore')
        classes_training = self.fillna(classes_training)
        classes_testing = classes_datasets[-1].drop("Method_ids", axis=1, errors='ignore')
        classes_testing = self.fillna(classes_testing, default='')
        file_names = classes_testing.pop("File").values.tolist()
        classes_names = classes_testing.pop("Class").values.tolist()
        print(list(zip(file_names, classes_names)))
        classes_testing_names = list(map("@".join, zip(file_names, [x if x in (False, True) else '' for x in classes_names])))
        return ClassificationInstance(classes_training, classes_testing, classes_testing_names, classes_dataset_dir)

    def extract_methods_datasets(self, methods_datasets):
        dataset_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Dataset'],
                         self.project.github()))
        methods_dataset_dir = os.path.join(dataset_dir, "methods")
        Path(methods_dataset_dir).mkdir(parents=True, exist_ok=True)
        methods_training = pd.concat(methods_datasets[:-1], ignore_index=True).drop("Method_ids", axis=1, errors='ignore')
        methods_training = self.fillna(methods_training)
        methods_testing = methods_datasets[-1]
        methods_testing =  self.fillna(methods_testing)
        methods_testing_names = methods_testing.pop("Method_ids").values.tolist()
        return ClassificationInstance(methods_training, methods_testing, methods_testing_names, methods_dataset_dir, label="BuggedMethods")

    def choose_versions(self, version_num=5, algorithm="bin", version_type=VersionType.Untyped, strict=True):
        self.extractor.choose_versions(version_num=version_num, algorithm=algorithm, strict=strict, version_type=version_type)

    def set_version_selection(self, version_num=5, algorithm="bin", version_type=VersionType.Untyped, strict=True, selected_config=0):
        self.extractor.choose_versions(version_num=version_num, algorithm=algorithm, strict=strict, version_type=version_type, selected_config=selected_config)
        self.extractor.selected_config = selected_config
        assert self.extractor.get_selected_versions()

    def save_data_names(self):
        j = list()
        out_path = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], "dataname.json"))
        for d in DataNameEnum:
            j.append(d.value.as_description_dict())
        with open(out_path, "w") as f:
            json.dump(j, f)

    def main(self):
        parser = argparse.ArgumentParser(description='Execute project data')
        parser.add_argument('-p', '--projects', dest='projects', action='store_const', const=True, default=False,
                            help='list all aleready defined projects')
        parser.add_argument('-c', '--choose', dest='choose', action='store', help='choose a project to extract')
        parser.add_argument('-g', '--github_repo_name', dest='github', action='store', help='the github repository name to the project to extract (lowercase)')
        parser.add_argument('-j', '--jira_name', dest='jira', action='store', help='the jira name to the project to extract (uppercase)')
        parser.add_argument('-עu', '--github_user_name', dest='github_user_name', action='store', help='the github user name to the project to extract (lowercase)', default="apache")
        parser.add_argument('-jl', '--jira_url', dest='jira_url', action='store', help='the link to jira', default="http://issues.apache.org/jira")
        parser.add_argument('-l', '--list_select_verions', dest='list_selected', action='store', help='the algorithm to select the versions : [bin]', default='bin')
        parser.add_argument('-s', '--select_verions', dest='select', action='store', help='the configuration to choose', default=-1, type=int)
        parser.add_argument('-n', '--num_verions', dest='num_versions', action='store', help='the number of versions to select', default=5, type=int)
        parser.add_argument('-t', '--versions_type', dest='versions_type', action='store', help='the versions type to select', default="Untyped")
        parser.add_argument('-f', '--free_choose', dest='free_choose', action='store_true', help='the versions type to select')
        args = parser.parse_args()
        self.github_user_name = args.github_user_name
        self.jira_url = args.jira_url
        if args.projects:
            self.list_projects()
        if args.choose:
            self.set_project_enum(args.choose)
        if args.github and args.jira:
            self.set_project(args.github, args.jira)
        if args.list_selected:
            self.choose_versions(version_num=args.num_versions, algorithm=args.list_selected, version_type=VersionType[args.versions_type], strict=args.free_choose)
        if args.select != -1:
            self.set_version_selection(version_num=args.num_versions, algorithm='bin',
                                 version_type=VersionType[args.versions_type], strict=args.free_choose, selected_config=args.select)
            self.extract()
            self.extract_metrics()


if __name__ == "__main__":
    m = Main()
    m.main()
