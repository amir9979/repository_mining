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

class Main():
    def __init__(self):
        self.project = None
        self.extractor = None
        self.save_data_names()
        self.jira_url = None
        self.github_user_name = None
        self.quick_mode = False

    def list_projects(self):
        print("\n".join(list(map(lambda e: "{0}: {1}".format(e.name, e.value.description), ProjectName))))

    def extract(self, selected_versions=True):
        self.extractor.extract(selected_versions)

    def set_project(self, github_name, github_user, jira_name, jira_url):
        self.project = Project(github_name, github_user, '', [jira_name], [], jira_url, '')
        self.set_extractor()

    def set_project_enum(self, name):
        self.project = ProjectName[name].value
        self.set_extractor()

    def set_extractor(self):
        self.extractor = DataExtractor(self.project, self.quick_mode)

    def extract_metrics(self, rest_versions, rest_only, data_types, predict=True):
        classes_datasets = []
        aggregated_classes_datasets = []
        methods_datasets = []
        rest_classes_datasets = []
        rest_aggregated_classes_datasets = []
        rest_methods_datasets = []
        selected_versions = self.extractor.get_selected_versions()[:-1]
        if not rest_only:
            for version in selected_versions:
                classes_df, methods_df, aggregated_classes_df = self.extract_features_to_version(version, True, data_types)
                classes_datasets.append(classes_df)
                methods_datasets.append(methods_df)
                aggregated_classes_datasets.append(aggregated_classes_df)
        for version in rest_versions:
            if version in selected_versions:
                continue
            try:
                classes_df, methods_df, aggregated_classes_df = self.extract_features_to_version(version, False, data_types)
                rest_classes_datasets.append((version, classes_df))
                rest_methods_datasets.append((version, methods_df))
                rest_aggregated_classes_datasets.append((version, aggregated_classes_df))
            except:
                traceback.print_exc()
        if rest_only:
            return
        try:
            training_datasets = aggregated_classes_datasets[:-1]
            classes_dataset = self.extract_classes_datasets(training_datasets, aggregated_classes_datasets[-1])
            if predict:
                classes_dataset.predict()
                for v, df in rest_aggregated_classes_datasets:
                    try:
                        self.extract_classes_datasets(training_datasets, df, v).predict()
                    except:
                        traceback.print_exc()
        except:
            traceback.print_exc()
        if not self.quick_mode:
            try:
                training_datasets = methods_datasets[:-1]
                methods_datasets = self.extract_methods_datasets(training_datasets, methods_datasets[-1]).predict()
                if predict:
                    methods_datasets.predict()
                    for v, df in rest_methods_datasets:
                        try:
                            self.extract_classes_datasets(training_datasets, df, v).predict()
                        except:
                            traceback.print_exc()
            except:
                traceback.print_exc()

    def create_all_but_one_dataset(self, data_types):
        alls = {}
        ones = {}
        detailed = {}
        for d in data_types:
            detailed[d] = []
        for d in DataNameEnum:
            data_type = d.value.data_type.value
            if data_type in data_types:
                detailed[data_type].append(d.value.name)
        for d in detailed:
            ones[d] = set(detailed[d])
            alls[d] = reduce(set.__or__, list(map(lambda x: set(detailed.get(x)), filter(lambda x: x != d, detailed.keys()))), set())

        dir_labels = []
        if self.quick_mode:
            dir_labels = [("classes", "bugged_Bugged")]
        else:
            dir_labels = [("methods", "bugged_methods_BuggedMethods"), ("classes", "bugged_Bugged")]
        for sub_dir, label in dir_labels:
            scores = []
            training_df = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "training.csv"), sep=';')
            testing_df = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "testing.csv"), sep=';')
            names = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "prediction.csv"), sep=';')[
                'name'].to_list()
            ci = ClassificationInstance(training_df, testing_df, names, self.get_dataset_path(sub_dir), label=label, save_all=False)
            try:
                ci.predict()
                ci_scores = dict(ci.scores)
                ci_scores.update({"type": "all_feature", "data_type": "all_feature"})
                scores.append(ci_scores)
            except Exception as e:
                print(e)

            for dir_name, columns in (('one', ones), ('all', alls)):
                training_df = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "training.csv"), sep=';')
                testing_df = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "testing.csv"), sep=';')
                dataset_cols = set(training_df.columns.to_list()).intersection(set(testing_df.columns.to_list()))
                names = pd.read_csv(os.path.join(self.get_dataset_path(sub_dir), "prediction.csv"), sep=';')['name'].to_list()

                ans = self.create_sub_data_set_by_columns(columns, dataset_cols, dir_name, label, names, sub_dir,
                                                          testing_df, training_df)
                if ans:
                    scores.extend(ans)
            pd.DataFrame(scores).to_csv(self.get_dataset_path(sub_dir + "_metrics.csv", False), index=False, sep=';')

    def create_sub_data_set_by_columns(self, columns, dataset_cols, dir_name, label, names, sub_dir, testing_df,
                                       training_df):
        scores = []
        for d in columns:
            cols = set(filter(lambda dc: any(map(lambda c: c in dc, columns[d])), dataset_cols))
            if len(cols) == 0:
                continue
            cols.add(label)
            cols = list(cols)
            train = training_df[cols]
            test = testing_df[cols]
            ci = ClassificationInstance(train, test, names, self.get_dataset_path(os.path.join(dir_name, sub_dir, d)),
                                        label=label)
            try:
                ci.predict()
                ci_scores = dict(ci.scores)
                ci_scores.update({"type": dir_name, "data_type": d})
                scores.append(ci_scores)
            except Exception as e:
                print(e)
        return scores

    def get_data_dirs(self):
        classes_data = Config.get_work_dir_path(os.path.join(Config().config['CACHING']['RepositoryData'],
                                                             Config().config['VERSION_METRICS']['ClassesData'],
                                                             self.project.github_name))
        method_data = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['MethodData'],
                         self.project.github_name))
        intermediate_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'],
                         Config().config['VERSION_METRICS']['Intermediate'],
                         self.project.github_name))
        classes_intermediate_dir = os.path.join(intermediate_dir, "classes")
        methods_intermediate_dir = os.path.join(intermediate_dir, "methods")
        for p in [intermediate_dir, classes_intermediate_dir, methods_intermediate_dir, classes_data, method_data]:
            Path(p).mkdir(parents=True, exist_ok=True)
        return classes_data, method_data, classes_intermediate_dir, methods_intermediate_dir, intermediate_dir

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
        columns_filter = ['File', 'Class', 'bugged_methods_BuggedMethods', 'Method', 'Method_ids']
        columns = list(
            filter(lambda x: x not in columns_filter, df.columns.values.tolist()))
        data = list()
        for key, group in df.groupby(groupby):
            key_data = {}
            key_data.update(dict(zip(groupby, key)))
            for feature in columns:
                pt = pd.DataFrame(group[feature].describe(include = 'all')).T
                cols = ["{0}_{1}".format(feature, c) for c in pt.columns.values.tolist()]
                pt.columns = cols
                key_data.update(list(pt.iterrows())[0][1].to_dict())
            data.append(key_data)
        return pd.DataFrame(data)

    def fillna(self, df, default=False):
        if 'bugged_Bugged' in df:
            df = df[df['bugged_Bugged'].notna()]
        if 'bugged_methods_BuggedMethods' in df :
            df = df[df['bugged_methods_BuggedMethods'].notna()]
        for col in df:
            dt = df[col].dtype
            if dt == int or dt == float:
                df[col].fillna(0, inplace=True)
            else:
                df[col].fillna(default, inplace=True)
        return df.dropna(axis=1)

    def extract_features_to_version(self, version, extract_bugs, data_types):
        self.extractor.checkout_version(version)
        db, extractors_to_run = self.get_extractors(data_types, extract_bugs, version)
        for extractor in extractors_to_run:
            start = time.time()
            try:
                extractor.extract()
                print(time.time() - start, extractor.__class__.__name__)
            except:
                traceback.print_exc()
                print(r"extractor {0} failed".format(extractor.__class__.__name__))
        classes_df, methods_df = db.build()
        aggregated_methods_df = self.aggrate_methods_df(methods_df)
        methods_df = self.fillna(methods_df)
        if self.quick_mode:
            aggregated_classes_df = classes_df
            aggregated_classes_df = self.fillna(aggregated_classes_df)
        else:
            aggregated_classes_df = self.merge_aggregated_methods_to_class(aggregated_methods_df, classes_df)
        classes_df = self.fillna(classes_df)
        methods_df = methods_df.drop('File', axis=1, errors='ignore')
        methods_df = methods_df.drop('Class', axis=1, errors='ignore')
        methods_df = methods_df.drop('Method', axis=1, errors='ignore')
        self.save_dfs(classes_df, methods_df, aggregated_classes_df, aggregated_methods_df, version)
        return classes_df, methods_df, aggregated_classes_df

    def merge_aggregated_methods_to_class(self, aggregated_methods_df, classes_df):
        aggregated_classes_df = classes_df.copy(deep=True)
        if 'Class' in aggregated_classes_df.columns and 'Class' in aggregated_methods_df.columns:
            aggregated_classes_df = aggregated_classes_df.merge(aggregated_methods_df, on=['File', 'Class'],
                                                                how='outer')
        else:
            aggregated_classes_df = aggregated_classes_df.merge(aggregated_methods_df, on=['File'], how='outer')
        return self.fillna(aggregated_classes_df)

    def save_to_csv(self, df, path):
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, sep=';')

    def save_dfs(self, classes_df, methods_df, aggregated_classes_df, aggregated_methods_df, version):
        classes_data, method_data, classes_intermediate_dir, methods_intermediate_dir, intermediate_dir = self.get_data_dirs()

        self.save_to_csv(classes_df, os.path.join(classes_intermediate_dir, version + ".csv"))
        self.save_to_csv(aggregated_classes_df, os.path.join(classes_intermediate_dir, version + "_aggregated_classes.csv"))

        self.save_to_csv(methods_df, os.path.join(methods_intermediate_dir, version + ".csv"))
        self.save_to_csv(aggregated_methods_df, os.path.join(intermediate_dir, version + "_aggregated_methods_df.csv"))

        self.save_to_csv(classes_df, os.path.join(classes_data, version + ".csv"))
        self.save_to_csv(aggregated_classes_df, os.path.join(classes_data, version + "_aggregated_classes_.csv"))
        self.save_to_csv(methods_df, os.path.join(method_data, version + ".csv"))

    def get_extractors(self, data_types, extract_bugs, version):
        db = DataBuilder(self.project, version)
        if extract_bugs:
            data_types.add("bugged")
            if not self.quick_mode:
                data_types.add("bugged_methods")
        extractors_to_run = set()
        for extractor in Extractor.get_all_extractors(self.project, version):
            if not extract_bugs and "bugged" in extractor.__class__.__name__.lower():
                continue
            extractor_data_types = []
            for dt in extractor.data_types:
                if dt.value in data_types:
                    extractor_data_types.append(dt)
                    extractors_to_run.add(extractor)
            db.add_data_types(extractor_data_types)
        return db, extractors_to_run

    def extract_classes_datasets(self, training_datasets, testing_dataset, sub_dir="classes"):
        training = pd.concat(training_datasets, ignore_index=True).drop(["File", "Class", "Method_ids"], axis=1, errors='ignore')
        training = self.fillna(training)
        testing = testing_dataset.drop(["Method_ids", "Class"], axis=1, errors='ignore')
        testing = self.fillna(testing, default='')
        file_names = testing.pop("File").values.tolist()
        # classes_names = testing.pop("Class").values.tolist()
        # classes_testing_names = list(map("@".join, zip(file_names, ['' if x in (False, True) else x for x in classes_names])))
        return ClassificationInstance(training, testing, file_names, self.get_dataset_path(sub_dir))

    def get_dataset_path(self, name, is_dir=True):
        dataset_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'], Config().config['VERSION_METRICS']['Dataset'],
                         self.project.github_name))
        path = os.path.join(dataset_dir, name)
        if is_dir:
            Path(path).mkdir(parents=True, exist_ok=True)
        else:
            Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        return path

    def extract_methods_datasets(self, training_datasets, testing_dataset):
        training = pd.concat(training_datasets, ignore_index=True).drop("Method_ids", axis=1, errors='ignore')
        training = self.fillna(training)
        testing = testing_dataset
        testing = self.fillna(testing)
        methods_testing_names = testing.pop("Method_ids").values.tolist()
        return ClassificationInstance(training, testing, methods_testing_names, self.get_dataset_path("methods"), label="bugged_methods_BuggedMethods")

    def choose_versions(self, version_num=5, algorithm="bin", version_type=VersionType.Untyped, strict=True):
        self.extractor.init_jira_commits()
        self.extractor.choose_versions(version_num=version_num, algorithm=algorithm, strict=strict, version_type=version_type)

    def set_version_selection(self, version_num=5, algorithm="bin", version_type=VersionType.Untyped, strict=True, selected_config=0):
        self.extractor.set_selected_config(selected_config)
        self.extractor.choose_versions(version_num=version_num, algorithm=algorithm, strict=strict, version_type=version_type)
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
        parser.add_argument('-g', '--github_repo_name', dest='github_repo', action='store', help='the github repository name to the project to extract (lowercase)')
        parser.add_argument('-j', '--jira_product_name', dest='jira_product', action='store', help='the jira name to the project to extract (uppercase)')
        parser.add_argument('-u', '--github_user_name', dest='github_user_name', action='store', help='the github user name to the project to extract (lowercase)', default="apache")
        parser.add_argument('-jl', '--jira_url', dest='jira_url', action='store', help='the link to jira', default="http://issues.apache.org/jira")
        parser.add_argument('-l', '--list_select_verions', dest='list_selected', action='store', help='the algorithm to select the versions : [bin]', default='bin')
        parser.add_argument('-d', '--data_types_to_extract', dest='data_types', action='store', help='Json file of the data types to extract as features. Choose a sublist of '
                                                                                                     '[checkstyle, designite_design, designite_implementation, '
                                                                                                     'designite_type_organic, designite_method_organic, designite_type_metrics,'
                                                                                                     'designite_method_metrics, source_monitor_files, source_monitor, ck, mood, halstead,'
                                                                                                     'jasome_files, jasome_methods, process_files, issues_files]. You can use the files under externals\configurations', default=r"externals\configurations\all.json")
        parser.add_argument('-s', '--select_verions', dest='select', action='store', help='the configuration to choose', default=0, type=int)
        parser.add_argument('-n', '--num_verions', dest='num_versions', action='store', help='the number of versions to select', default=3, type=int)
        parser.add_argument('-t', '--versions_type', dest='versions_type', action='store', help='the versions type to select', default="Untyped")
        parser.add_argument('-f', '--free_choose', dest='free_choose', action='store_true', help='the versions type to select')
        parser.add_argument('-r', '--only_rest', dest='only_rest', action='store_true', help='extract only rest versions')
        parser.add_argument('-a', '--all_rest', dest='all_rest', action='store_true', help='extract for all versions in the projects')
        parser.add_argument('-q', '--quick_mode', dest='quick_mode', action='store_true', help='quick_mode')
        parser.add_argument('rest', nargs=argparse.REMAINDER)
        args = parser.parse_args()
        self.quick_mode = args.quick_mode
        print(vars(args))
        self.github_user_name = args.github_user_name
        self.jira_url = args.jira_url
        if args.projects:
            self.list_projects()
        if args.choose:
            self.set_project_enum(args.choose)
        if args.github_repo and args.jira_product:
            self.set_project(args.github_repo, args.github_user_name, args.jira_product, args.jira_url)
        if args.list_selected:
            self.choose_versions(version_num=args.num_versions, algorithm=args.list_selected, version_type=VersionType[args.versions_type], strict=args.free_choose)
        if args.select == -1:
            self.set_version_selection(version_num=args.num_versions, algorithm='bin',
                                       version_type=VersionType[args.versions_type], strict=args.free_choose, selected_config=0)
            self.extract()
        else:
            self.set_version_selection(version_num=args.num_versions, algorithm='bin',
                                       version_type=VersionType[args.versions_type], strict=args.free_choose, selected_config=args.select)
            rest = args.rest
            predict_all = True
            if args.all_rest:
                predict_all = False
                rest = list(map(lambda v: v._name, self.extractor.get_versions_by_type()))
            self.extract()
            data_types = None
            if os.path.exists(args.data_types):
                with open(args.data_types) as f:
                    data_types = set(json.loads(f.read()))
            self.extract_metrics(rest, args.only_rest, data_types, True)
            if predict_all:
                self.create_all_but_one_dataset(data_types)


if __name__ == "__main__":
    m = Main()
    m.main()
