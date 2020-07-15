import logging
from multiprocessing import Pool

import numpy as np
import os
import pandas as pd
from abc import ABC, abstractmethod
from imblearn.over_sampling import SMOTE
from sklearn import preprocessing
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, chi2, mutual_info_classif, f_classif, SelectFromModel, RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

from config import Config
from paper.builders import Builders
from paper.utils import FeatureSelectionHelper, EstimatorSelectionHelper
from projects import ProjectName


class Analysis(ABC):
    models = {
        'LinearDiscriminantAnalysis': LinearDiscriminantAnalysis(),
        'QuadraticDiscriminantAnalysis': QuadraticDiscriminantAnalysis(),
        'LogisticRegression': LogisticRegression(),
        'BernoulliNaiveBayes': BernoulliNB(),
        'K-NearestNeighbor': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(),
        'RandomForest': RandomForestClassifier(),
        'SupportVectorMachine': SVC(),
        'MultilayerPerceptron': MLPClassifier()
    }

    params = {
        'LinearDiscriminantAnalysis': {},
        'QuadraticDiscriminantAnalysis': {},
        'LogisticRegression': {'C': list(np.logspace(-4, 4, 3))},
        'BernoulliNaiveBayes': {},
        'K-NearestNeighbor': {},
        'DecisionTree': {'criterion': ['gini', 'entropy'], },
        'RandomForest': {'n_estimators': [10, 100]},
        'SupportVectorMachine': {'C': [0.1, 100]},
        'MultilayerPerceptron': {'hidden_layer_sizes': [(17, 8, 17)],
                                 'activation': ['tanh', 'relu']}
    }

    selection_methods = {
        'chi2_20p': SelectPercentile(chi2, percentile=20),
        'chi2_50p': SelectPercentile(chi2, percentile=50),
        'mutual_info_classif_20p': SelectPercentile(mutual_info_classif, percentile=20),
        'mutual_info_classif_50p': SelectPercentile(mutual_info_classif, percentile=50),
        'f_classif_20': SelectPercentile(f_classif, percentile=20),
        'f_classif_50': SelectPercentile(f_classif, percentile=50),
        'recursive_elimination': RFECV(RandomForestClassifier(), min_features_to_select=3, step=1, cv=5, scoring='f1')
    }

    def __init__(self, log_name, project: ProjectName, metric: str):
        self.logs = Logs(log_name)
        self.project = project
        self.project_name = project.github()
        self.metric = metric
        self.versions = self._get_versions()
        self.caching = Caching(self.project_name, self.metric)

    def _get_versions(self):
        self.logs.general("{0} | {1} | 1/11 | Getting Versions ...".format(self.metric, self.project_name))
        versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
        versions_path = os.path.join(versions_dir, self.project_name + ".csv")
        versions = pd.read_csv(versions_path)['version'].to_list()
        self.logs.success("{0} | {1} | 1/11 | Got Versions.".format(self.metric, self.project_name))
        return versions

    def analyse(self):
        try:
            datasets = self.build_datasets(self.versions)
            training_df, testing_df = self.split_dataset(datasets)
            training_df, testing_df = self.handle_missing_values(training_df, testing_df)
            selected_features, selected_training = self.select_features(training_df)
            oversampled_training = self.oversample(selected_training, training_df)
            selected_testing = self.get_selected_testing(testing_df, selected_features)
            summaries = self.hyper_parameterize(oversampled_training)
            top_summaries = self.get_top_summaries(summaries)
            configurations = self.get_configurations(top_summaries)
            self.calculate_scores(configurations, oversampled_training, selected_testing)
            self.logs.summary("{0} | {1} | project succeeded.".format(self.metric, self.project_name))

        except Analysis.FailedBuildDataset:
            self.logs.failure("{0} | {1} | 2/11 | Failed BUILDING dataset".format(self.metric, self.project_name),
                              verbose=True)
            self.logs.summary("{0} | {1} | project failed.".format(self.metric, self.project_name))
            return

        except Analysis.FailedSplit:
            self.logs.failure("{0} | {1} | 3/11 | There are missing datasets".format(self.metric, self.project_name))
            self.logs.summary("{0} | {1} | project failed.".format(self.metric, self.project_name))
            return

        except:
            self.logs.failure("{0} | {1} | Failed to analyse project".format(self.metric, self.project_name),
                              verbose=True)
            self.logs.summary("{0} | {1} | project failed.".format(self.metric, self.project_name))
            return

    @abstractmethod
    def build_datasets(self, versions):
        self.logs.general("{0} | {1} | 2/11 | Building Datasets ...".format(self.metric, self.project_name))
        pass

    def split_dataset(self, datasets):
        self.logs.general("{0} | {1} | 3/11 | Splitting dataset ...".format(self.metric, self.project_name))
        if any(dataset is None for dataset in datasets):
            raise Analysis.FailedSplit()
        training_df = pd.concat(datasets[:-1], ignore_index=True).drop(["File", "Class"], axis=1)
        testing_df = datasets[-1].drop(["File", "Class"], axis=1)
        self.caching.store_datasets(training_df, testing_df)
        self.logs.success("{0} | {1} | 3/11 | Splitted training and testing datasets.".format(self.metric, self.project_name))
        return training_df, testing_df

    class FailedSplit(Exception):
        pass

    @abstractmethod
    def handle_missing_values(self, training_df, testing_df):
        self.logs.general("{0} | {1} | 4/11 | Handling missing values".format(self.metric, self.project_name))
        pass

    def select_features(self, training_df):
        self.logs.general("{0} | {1} | 5/11 | Selecting Features ...".format(self.metric, self.project_name))
        dataset = pd.DataFrame.copy(training_df)
        y = dataset.pop('Bugged').values
        X = dataset.values
        features = dataset.columns
        selector = FeatureSelectionHelper(self.selection_methods, features)
        selector.select(X, y)
        selected_features = selector.get_selected_features()
        selected_dataset = selector.get_selected_dataset()
        self.caching.store_selected_features(selected_features, selected_dataset)
        self.logs.success("{0} | {1} | 5/11 | Selected Versions.".format(self.metric, self.project_name))
        return selected_features, selected_dataset

    def oversample(self, selected_datasets, training_df):
        self.logs.general("{0} | {1} | 6/11 | Oversampling dataset ...".format(self.metric, self.project_name))
        y = training_df['Bugged'].values
        oversampled_datasets = {method: SMOTE().fit_resample(X, y) for method, X in selected_datasets.items()}
        self.caching.store_oversamples(oversampled_datasets)
        self.logs.success("{0} | {1} | 6/11 | Oversampled dataset.".format(self.metric, self.project_name))
        return oversampled_datasets

    def hyper_parameterize(self, oversample_datasets):
        def get_summary(X, y):
            helper = EstimatorSelectionHelper(self.models, self.params)
            helper.fit(X, y)
            return helper.score_summary()
        self.logs.general("{0} | {1} | 7/11 | Tuning models and parameters ...".format(self.metric, self.project_name))
        summaries = {method: get_summary(data[0], data[1])
                     for method, data in oversample_datasets.items()}
        self.caching.store_summaries(summaries)
        self.logs.success("{0} | {1} | 7/11 | Tuned models and parameters.".format(self.metric, self.project_name))
        return summaries

    def get_top_summaries(self, summaries, n=10):
        self.logs.general("{0} | {1} | 8/11 | Getting Top Summaries ...".format(self.metric, self.project_name))
        top_summaries = {method: summary[:n] for method, summary in summaries.items()}
        self.caching.store_top_summaries(top_summaries)
        self.logs.success("{0} | {1} | 8/11 | Got Top Summaries.".format(self.metric, self.project_name))
        return top_summaries

    def get_configurations(self, top_summaries):
        self.logs.general("{0} | {1} | 9/11 | Getting Configurations ...".format(self.metric, self.project_name))
        configurations = {method: list(map(lambda x: x[1].to_dict(),
                                           top_summary.drop(EstimatorSelectionHelper.get_scores_info(),
                                                            axis=1)
                                           .where(pd.notnull(top_summary), None).iterrows()))
                          for method, top_summary in top_summaries.items()}
        self.logs.success("{0} | {1} | 9/11 | Got Configurations.".format(self.metric, self.project_name))
        return configurations

    def get_selected_testing(self, testing_df, selected_features):
        self.logs.general("{0} | {1} | 10/11 | Get Selected Testing Dataset ...".format(self.metric, self.project_name))
        testing_y = testing_df.pop('Bugged').values
        selected_testing_datasets = {
            method: (testing_df[testing_df.columns.intersection(features)].values, testing_y)
            for method, features in selected_features.items()
        }
        self.caching.store_selected_testing_datasets(selected_testing_datasets)
        self.logs.success("{0} | {1} | 10/11 | Got Selected Testing Dataset.".format(self.metric, self.project_name))
        return selected_testing_datasets

    def calculate_scores(self, configurations, oversampled_training, selected_testing):
        def calculate_score(method_name, training, testing, configuration):
            estimator = self.models[configuration['estimator']]
            params = {key: val for key, val in configuration.items() if not (val is None or key == 'estimator')}
            estimator.set_params(**params)
            training_X, training_y = training
            estimator.fit(training_X, training_y)
            testing_X, testing_y = testing
            prediction_y = estimator.predict(testing_X)
            scores_dict = {
                'estimator': configuration['estimator'],
                'configuration': str(params),
                'feature_selection': method_name,
                'precision': precision_score(testing_y, prediction_y),
                'recall': recall_score(testing_y, prediction_y),
                'f1-measure': f1_score(testing_y, prediction_y),
                'auc-roc': roc_auc_score(testing_y, prediction_y),
                'brier score': brier_score_loss(testing_y, prediction_y)
            }
            return scores_dict

        self.logs.general("{0} | {1} | 11/11 | Calculate Scores ...".format(self.metric, self.project_name))
        method_names = configurations.keys()
        scores_dicts = list(map(lambda method_name:
                          list(map(lambda configuration:
                                   calculate_score(method_name,
                                                   oversampled_training[method_name],
                                                   selected_testing[method_name],
                                                   configuration),
                                   configurations[method_name])), method_names))
        scores_df = [pd.DataFrame(score) for score in scores_dicts]
        scores = pd.concat(scores_df)
        self.caching.store_scores(scores)
        self.logs.success("{0} | {1} | 11/11 | Calculated Scores.".format(self.metric, self.project_name))
        return scores

    class FailedBuildDataset(Exception):
        pass


class Designite(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "designite")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_designite_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Designite Smells dataset is empty.")
            return classes_df
        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        super().handle_missing_values(training_df, testing_df)
        training_df = training_df.dropna().astype(int)
        testing_df = testing_df.dropna().astype(int)
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class Fowler(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "fowler")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_fowler_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Fowler Smells dataset is empty.")

            def union_smell(value):
                return any(value)

            aggregation_fns = {feature: union_smell for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            classes_df.dropna(inplace=True)
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.fillna(False, inplace=True)
            return dataset

        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        super().handle_missing_values(training_df, testing_df)
        training_df = training_df.dropna().astype(int)
        testing_df = testing_df.dropna().astype(int)
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class Traditional(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "traditional")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_traditional_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Traditional Metrics dataset is empty.")

            def mean_or_union(rows):
                try:
                    return np.mean(rows)
                except TypeError as e:
                    rows = rows.astype('int64')
                    return np.mean(rows)

            classes_df.dropna(inplace=True)
            values = {feature: 0 for feature in list(methods_df.columns)}
            values.update(dict(zip(('File', 'Class', 'Method'), ['nan']*3)))
            methods_df.fillna(value=values, inplace=True)
            methods_df.dropna(inplace=True)
            aggregation_fns = {feature: mean_or_union for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.dropna(subset=['Bugged'], inplace=True)
            dataset.fillna(0, inplace=True)
            return dataset
        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        def scale(dataset):
            X = preprocessing.MinMaxScaler().fit_transform(dataset.drop("Bugged", axis=1).values)
            y = dataset['Bugged']
            dataset = pd.DataFrame(X, columns=dataset.drop("Bugged", axis=1).columns)
            dataset.insert(len(dataset.columns), "Bugged", y.to_list())
            return dataset
        training_df = scale(training_df.dropna().astype(int))
        testing_df = scale(testing_df.dropna().astype(int))
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class DesigniteFowler(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "designite_fowler")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_designite_fowler_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Designite+Fowler Smells dataset is empty.")

            def union_smell(value):
                return any(value)

            aggregation_fns = {feature: union_smell for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            classes_df.dropna(inplace=True)
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.fillna(False, inplace=True)
            return dataset

        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        training_df = training_df.dropna().astype(int)
        testing_df = testing_df.dropna().astype(int)
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class DesigniteTraditional(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "designite_traditional")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_designite_traditional_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Traditional Metrics dataset is empty.")

            def mean_or_union(rows):
                try:
                    return np.mean(rows)
                except TypeError as e:
                    rows = rows.astype('int64')
                    return np.mean(rows)

            classes_df.dropna(inplace=True)
            values = {feature: 0 for feature in list(methods_df.columns)}
            values.update(dict(zip(('File', 'Class', 'Method'), ['nan']*3)))
            methods_df.fillna(value=values, inplace=True)
            methods_df.dropna(inplace=True)
            aggregation_fns = {feature: mean_or_union for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.dropna(subset=['Bugged'], inplace=True)
            dataset.fillna(0, inplace=True)
            return dataset
        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        def scale(dataset):
            X = preprocessing.MinMaxScaler().fit_transform(dataset.drop("Bugged", axis=1).values)
            y = dataset['Bugged']
            dataset = pd.DataFrame(X, columns=dataset.drop("Bugged", axis=1).columns)
            dataset.insert(len(dataset.columns), "Bugged", y.to_list())
            return dataset
        training_df = scale(training_df.dropna().astype(int))
        testing_df = scale(testing_df.dropna().astype(int))
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class FowlerTraditional(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
       super().__init__(log_name, project, "fowler_traditional")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_fowler_traditional_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty:
                raise Analysis.FailedBuildDataset("Fowler+Traditional Metrics dataset is empty.")

            def mean_or_union(rows):
                if rows.dtypes.name == 'bool':
                    return any(rows)
                try:
                    return np.mean(rows)
                except TypeError as e:
                    rows = rows.astype('int64')
                    return np.mean(rows)

            # file-class conversion leaves rows without values(nan) - drop them
            classes_df.dropna(inplace=True)
            values = {feature: 0 for feature in list(methods_df.columns)}
            values.update(dict(zip(('File', 'Class', 'Method'), ['nan']*3)))
            methods_df.fillna(value=values, inplace=True)
            methods_df.dropna(inplace=True)
            aggregation_fns = {feature: mean_or_union for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.dropna(inplace=True)
            return dataset

        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        def scale(dataset):
            X = preprocessing.MinMaxScaler().fit_transform(dataset.drop("Bugged", axis=1).values)
            y = dataset['Bugged']
            dataset = pd.DataFrame(X, columns=dataset.drop("Bugged", axis=1).columns)
            dataset.insert(len(dataset.columns), "Bugged", y.to_list())
            return dataset
        training_df = scale(training_df.dropna().astype(int))
        testing_df = scale(testing_df.dropna().astype(int))
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class DesigniteFowlerTraditional(Analysis):
    def __init__(self, log_name: str, project: ProjectName):
        super().__init__(log_name, project, "designite_fowler_traditional")

    def build_datasets(self, versions):
        def build_dataset(version):
            db = Builders.get_designite_fowler_traditional_builder(self.project, version)
            classes_df, methods_df = db.build()
            if classes_df.empty or methods_df.empty:
                raise Analysis.FailedBuildDataset("Designite+Fowler+Traditional Metrics dataset is empty.")

            def mean_or_union(rows):
                if rows.dtypes.name == 'bool':
                    return any(rows)
                try:
                    return np.mean(rows)
                except TypeError as e:
                    rows = rows.astype('int64')
                    return np.mean(rows)

            # file-class conversion leaves rows without values(nan) - drop them
            classes_df.dropna(inplace=True)
            values = {feature: 0 for feature in list(methods_df.columns)}
            values.update(dict(zip(('File', 'Class', 'Method'), ['nan'] * 3)))
            methods_df.fillna(value=values, inplace=True)
            methods_df.dropna(inplace=True)
            aggregation_fns = {feature: mean_or_union for feature in list(methods_df.columns)[3:]}
            aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
            dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
            dataset.dropna(inplace=True)
            return dataset

        super().build_datasets(versions)
        datasets = list(map(build_dataset, versions))
        self.logs.success("{0} | {1} | 2/11 | Built Datasets.".format(self.metric, self.project_name))
        return datasets

    def handle_missing_values(self, training_df, testing_df):
        def scale(dataset):
            X = preprocessing.MinMaxScaler().fit_transform(dataset.drop("Bugged", axis=1).values)
            y = dataset['Bugged']
            dataset = pd.DataFrame(X, columns=dataset.drop("Bugged", axis=1).columns)
            dataset.insert(len(dataset.columns), "Bugged", y.to_list())
            return dataset
        training_df = scale(training_df.dropna().astype(int))
        testing_df = scale(testing_df.dropna().astype(int))
        self.logs.success("{0} | {1} | 4/11 | Handling missing values.".format(self.metric, self.project_name))
        return training_df, testing_df


class Caching:
    def __init__(self, project_name, metric):
        self.base = Config.get_work_dir_path(os.path.join("paper", "analysis"))
        Config.assert_dir_exists(self.base)
        self.project_name = project_name
        self.metric = metric

    def store_datasets(self, training_df, testing_df):
        datasets_dir = os.path.join(self.base, self.metric, self.project_name, "dataset")
        Config.assert_dir_exists(datasets_dir)
        training_path = os.path.join(datasets_dir, "training.csv")
        testing_path = os.path.join(datasets_dir, "testing.csv")
        training_df.to_csv(training_path, index=False)
        testing_df.to_csv(testing_path, index=False)

    def store_selected_features(self, selected_features, selected_dataset):
        for method in selected_features.keys():
            selected_dir = os.path.join(self.base, self.metric, self.project_name, "selected_features", method)
            Config.assert_dir_exists(selected_dir)
            features_path = os.path.join(selected_dir, "features.csv")
            dataset_path = os.path.join(selected_dir, "dataset.csv")
            pd.DataFrame(selected_features[method]).to_csv(features_path, index=False)
            pd.DataFrame(selected_dataset[method]).to_csv(dataset_path, index=False)

    def store_oversamples(self, oversampled_datasets):
        for method in oversampled_datasets.keys():
            oversamples_dir = os.path.join(self.base, self.metric, self.project_name, "oversamples")
            Config.assert_dir_exists(oversamples_dir)
            path = os.path.join(oversamples_dir, method + ".csv")
            pd.DataFrame(oversampled_datasets[method]).to_csv(path, index=False)

    def store_summaries(self, summaries):
        for method in summaries.keys():
            summaries_dir = os.path.join(self.base, self.metric, self.project_name, "score_summary")
            Config.assert_dir_exists(summaries_dir)
            path = os.path.join(summaries_dir, method + ".csv")
            summaries[method].to_csv(path, index=False)

    def store_top_summaries(self, top_summaries):
        for method in top_summaries.keys():
            top_summaries_dir = os.path.join(self.base, self.metric, self.project_name, "top_scores_summary")
            Config.assert_dir_exists(top_summaries_dir)
            path = os.path.join(top_summaries_dir, method + ".csv")
            top_summaries[method].to_csv(path, index=False)

    def store_selected_testing_datasets(self, selected_testing_datasets):
        for method in selected_testing_datasets.keys():
            testing_dataset_dir = os.path.join(self.base, self.metric, self.project_name, "selected_testing_X")
            Config.assert_dir_exists(testing_dataset_dir)
            path = os.path.join(testing_dataset_dir, method + ".csv")
            pd.DataFrame(selected_testing_datasets[method]).to_csv(path, index=False)

    def store_scores(self, score):
        scores_dir = os.path.join(self.base, self.metric, self.project_name)
        Config.assert_dir_exists(scores_dir)
        path = os.path.join(scores_dir, "scores.csv")
        score.to_csv(path, index=False)


class Logs:
    def __init__(self, log_name):
        self.log_name = log_name
        self._get_loggers()
        self._set_loggers_level()
        self._create_formatters()
        self._create_handlers()
        self._set_formatters_to_handlers()
        self._set_handlers_levels()
        self._set_handlers_to_loggers()

    def success(self, message):
        self.success_log.info(message)

    def failure(self, message, verbose=False):
        if verbose:
            self.failure_verbose_log.exception(message)
        self.failure_log.error(message)

    def general(self, message):
        self.general_log.info(message)

    def summary(self, message):
        self.summary_log.info(message)

    def _get_loggers(self):
        self.general_log = logging.getLogger(self.log_name + 'general')
        self.summary_log = logging.getLogger(self.log_name + 'summary')
        self.success_log = logging.getLogger(self.log_name + 'success')
        self.failure_log = logging.getLogger(self.log_name + 'failure')
        self.failure_verbose_log = logging.getLogger(self.log_name + 'failure_verbose')

    def _set_loggers_level(self):
        self.general_log.setLevel(logging.INFO)
        self.summary_log.setLevel(logging.INFO)
        self.success_log.setLevel(logging.INFO)
        self.failure_log.setLevel(logging.ERROR)
        self.failure_verbose_log.setLevel(logging.ERROR)

    def _create_formatters(self):
        self.console_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(message)s'
        )

        self.file_formatter = logging.Formatter(
            '%(asctime)s | %(message)s'
        )

    def _create_handlers(self):
        self.console = logging.StreamHandler()
        paper_dir = Config.get_work_dir_path(os.path.join("paper", "logs"))
        self.general_file = logging.FileHandler(os.path.join(paper_dir, self.log_name + "_general.log"), "a")
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, self.log_name + "_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, self.log_name + "_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, self.log_name + "_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir,
                                                                     self.log_name + "_failure_verbose.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.general_file.setFormatter(self.console_formatter)
        self.summary_file.setFormatter(self.file_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)
        self.failure_verbose_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.general_file.setLevel(logging.INFO)
        self.summary_file.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)
        self.failure_verbose_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        if not self.general_log.hasHandlers():
            self.general_log.addHandler(self.console)
            self.general_log.addHandler(self.general_file)

        if not self.summary_log.hasHandlers():
            self.summary_log.addHandler(self.summary_file)

        if not self.success_log.hasHandlers():
            self.success_log.addHandler(self.console)
            self.success_log.addHandler(self.success_file)

        if not self.failure_log.hasHandlers():
            self.failure_log.addHandler(self.console)
            self.failure_log.addHandler(self.failure_file)

        if not self.failure_verbose_log.hasHandlers():
            self.failure_verbose_log.addHandler(self.console)
            self.failure_verbose_log.addHandler(self.failure_verbose_file)


def run(project):
    log_name = "analysis"
    # Designite(log_name, project).analyse()
    Fowler(log_name, project).analyse()
    DesigniteFowler(log_name, project).analyse()
    Traditional(log_name, project).analyse()
    DesigniteTraditional(log_name, project).analyse()
    # FowlerTraditional(log_name, project).analyse()
    # DesigniteFowlerTraditional(log_name, project).analyse()


if __name__ == "__main__":
    projects = list(ProjectName)
    # projects = [
    #     ProjectName.Camel,
        # ProjectName.CommonsBeanUtils,
        # ProjectName.Drill,
        # ProjectName.FOP,
        # ProjectName.Continuum,
        # ProjectName.OpenJPA,
        # ProjectName.Jackrabbit,
        # ProjectName.Tapestry5,
        # ProjectName.CommonsJexl,
        # ProjectName.CXF,
        # ProjectName.Shiro,
        # ProjectName.Reef,
        # ProjectName.Olingo,
        # ProjectName.Accumulo,
        # ProjectName.Cocoon,
        # ProjectName.Cayenne,
        # ProjectName.Kafka,
        # ProjectName.CarbonData,
        # ProjectName.Giraph,
        # ProjectName.Isis,
        # ProjectName.Wicket,
        # ProjectName.Beam,
        # ProjectName.TinkerPop
    # ]
    with Pool() as p:
       p.map(run, projects)

