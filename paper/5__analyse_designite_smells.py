import functools
import logging
import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.base import clone
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, chi2, mutual_info_classif, f_classif, SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

from config import Config
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataNameEnum
from paper.utils import EstimatorSelectionHelper, FeatureSelectionHelper
from projects import ProjectName

done = []


def build_dataset(version, project):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    try:
        db = DataBuilder(project, version)

        db.append(DataNameEnum.ImperativeAbstraction)
        db.append(DataNameEnum.MultifacetedAbstraction)
        db.append(DataNameEnum.UnnecessaryAbstraction)
        db.append(DataNameEnum.UnutilizedAbstraction)
        db.append(DataNameEnum.DeficientEncapsulation)
        db.append(DataNameEnum.UnexploitedEncapsulation)
        db.append(DataNameEnum.BrokenModularization)
        db.append(DataNameEnum.Cyclic_DependentModularization)
        db.append(DataNameEnum.InsufficientModularization)
        db.append(DataNameEnum.Hub_likeModularization)
        db.append(DataNameEnum.BrokenHierarchy)
        db.append(DataNameEnum.CyclicHierarchy)
        db.append(DataNameEnum.DeepHierarchy)
        db.append(DataNameEnum.MissingHierarchy)
        db.append(DataNameEnum.MultipathHierarchy)
        db.append(DataNameEnum.RebelliousHierarchy)
        db.append(DataNameEnum.WideHierarchy)
        db.append(DataNameEnum.Bugged)

        general_log.info("{0} | {1} | building dataset".format(
            project.github(),
            version
        ))
        classes_df, methods_df = db.build()
        if not classes_df.empty:
            success_log.info("{0} | {1} | succeeded building dataset".format(
                project.github(),
                version
            ))
        else:
            raise Exception("Designite smells dataset is empty.")

        return classes_df
    except Exception:
        failure_log.error("{0} | {1} | (exception) failed building dataset".format(
            project.github(),
            version
        ))

        failure_verbose_log.exception("{0} | {1} | failed building dataset".format(
            project.github(),
            version
        ))
        return None


def extract_datasets(project):
    general_log = logging.getLogger(__name__)
    failure_log = logging.getLogger("failure")
    summary_log = logging.getLogger("summary")

    general_log.info("{0} | Getting versions ...".format(project.github()))

    versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
    versions_path = os.path.join(versions_dir, project.github() + ".csv")
    versions = pd.read_csv(versions_path)['version'].to_list()

    general_log.info("{0} | Building dataset ...".format(project.github()))
    build = functools.partial(build_dataset, project=project)
    datasets = list(map(build, versions))

    if any(dataset is None for dataset in datasets):
        failure_log.error("{0} | There are missing datasets".format(project.github()))
        summary_log.info("{0} | project failed.".format(project.github()))
        return

    dataset_dir = Config.get_work_dir_path(os.path.join("paper", "datasets", "designite", project.github()))
    Path(dataset_dir).mkdir(parents=True, exist_ok=True)
    training_path = os.path.join(dataset_dir, "training.csv")
    testing_path = os.path.join(dataset_dir, "testing.csv")

    pd.concat(datasets[:-1], ignore_index=True).drop(["File", "Class"], axis=1).to_csv(training_path, index=False)
    datasets[-1].drop(["File", "Class"], axis=1).to_csv(testing_path, index=False)


def execute(project):
    dataset_dir = Config.get_work_dir_path(os.path.join("paper", "datasets", "designite", project.github()))
    Path(dataset_dir).mkdir(parents=True, exist_ok=True)
    training_path = os.path.join(dataset_dir, "training.csv")
    testing_path = os.path.join(dataset_dir, "testing.csv")

    training_df = pd.read_csv(training_path).dropna().astype(int)
    testing_df = pd.read_csv(testing_path).dropna().astype(int)

    original_training_y = training_df.pop('Bugged').values
    original_training_X = training_df.values

    testing_y = testing_df.pop('Bugged').values
    testing_X = testing_df.values

    selection_methods = {
        'chi2_10p': SelectPercentile(chi2, percentile=10),
        'chi2_20p': SelectPercentile(chi2, percentile=20),
        'chi2_50p': SelectPercentile(chi2, percentile=50),
        'mutual_info_classif_10p': SelectPercentile(mutual_info_classif, percentile=10),
        'mutual_info_classif_20p': SelectPercentile(mutual_info_classif, percentile=20),
        'mutual_info_classif_50p': SelectPercentile(mutual_info_classif, percentile=50),
        'f_classif_10': SelectPercentile(f_classif, percentile=10),
        'f_classif_20': SelectPercentile(f_classif, percentile=20),
        'f_classif_50': SelectPercentile(f_classif, percentile=50),
        'linear_svc': SelectFromModel(LinearSVC(C=0.01, penalty="l1", dual=False))
    }

    features = training_df.columns
    selector = FeatureSelectionHelper(selection_methods, features)
    selector.select(original_training_X, original_training_y)
    features = selector.get_selected_features()
    data = selector.get_selected_dataset()

    columns = ['estimator', 'configuration', 'feature_selection', 'precision', 'recall', 'f1-measure', 'auc-roc',
               'brier score']
    scores = pd.DataFrame(columns=columns)

    for method_name, training_X in data.items():
        training_y = original_training_y
        oversample = SMOTE()
        training_X, training_y = oversample.fit_resample(training_X, training_y)

        models = {
            'LinearDiscriminantAnalysis': LinearDiscriminantAnalysis(),
            # 'QuadraticDiscriminantAnalysis': QuadraticDiscriminantAnalysis(),
            # 'LogisticRegression': LogisticRegression(),
            # 'BernoulliNaiveBayes': BernoulliNB(),
            # 'K-NearestNeighbor': KNeighborsClassifier(),
            # 'DecisionTree': DecisionTreeClassifier(),
            # 'RandomForest': RandomForestClassifier(),
            # 'SupportVectorMachine': SVC(),
            # 'MultilayerPerceptron': MLPClassifier()
        }
        params = {
            'LinearDiscriminantAnalysis': {},
            # 'QuadraticDiscriminantAnalysis': {},
            # 'LogisticRegression': {'C': list(np.logspace(-4, 4, 3))},
            # 'BernoulliNaiveBayes': {},
            # 'K-NearestNeighbor': {},
            # 'DecisionTree': {'criterion': ['gini', 'entropy'], },
            # 'RandomForest': {'n_estimators': [10, 100]},
            # 'SupportVectorMachine': {'C': [0.1, 100]},
            # 'MultilayerPerceptron': {'hidden_layer_sizes': [(17, 8, 17)],
            #                          'activation': ['tanh', 'relu']}
        }

        helper = EstimatorSelectionHelper(models, params)
        helper.fit(training_X, training_y, scoring='f1')
        summary = helper.score_summary()
        top_summary = summary[:10]
        top_summary_iter = top_summary.drop(EstimatorSelectionHelper.get_scores_info(), axis=1) \
            .where(pd.notnull(top_summary), None) \
            .iterrows()

        models_info = list(map(lambda x: x[1].to_dict(), top_summary_iter))

        selected_testing_X = testing_df[testing_df.columns.intersection(features[method_name])].values

        predictions = []
        for model_info in models_info:
            # TODO Cloning also copies the parameters. That is not what I want.
            estimator = clone(models[model_info['estimator']])
            params = {key: val for key, val in model_info.items() if not (val is None or key == 'estimator')}
            estimator.set_params(**params)
            estimator.fit(training_X, training_y)
            prediction_y = estimator.predict(selected_testing_X)
            predictions.append(prediction_y)
            scores_dict = {
                'estimator': model_info['estimator'],
                'configuration': str(params),
                'feature_selection': method_name,
                'precision': precision_score(testing_y, prediction_y),
                'recall': recall_score(testing_y, prediction_y),
                'f1-measure': f1_score(testing_y, prediction_y),
                'auc-roc': roc_auc_score(testing_y, prediction_y),
                'brier score': brier_score_loss(testing_y, prediction_y)
            }
            scores = scores.append(scores_dict, ignore_index=True)
    pass
    scores_dir = Config.get_work_dir_path(os.path.join("paper", "scores", "designite", project.github()))
    Path(scores_dir).mkdir(parents=True, exist_ok=True)
    scores_path = os.path.join(scores_dir, "scores.csv")
    feature_selection_dir = os.path.join(scores_dir, 'feature_selection')
    features_dir = os.path.join(feature_selection_dir, 'features')
    training_dir = os.path.join(feature_selection_dir, 'training_x')
    Path(features_dir).mkdir(parents=True, exist_ok=True)
    Path(training_dir).mkdir(parents=True, exist_ok=True)
    for method_name, training_X in data.items():
        features_path = os.path.join(features_dir, method_name + ".csv")
        pd.DataFrame({'Features': features[method_name]}).to_csv(features_path, index=False)
        training_x_path = os.path.join(training_dir, method_name + ".csv")
        pd.DataFrame(data=training_X, columns=features[method_name]).to_csv(training_x_path, index=False)

    training_y_path = os.path.join(scores_dir, "training_y.csv")
    testing_x_path = os.path.join(scores_dir, "testing_x.csv")
    testing_y_path = os.path.join(scores_dir, "testing_y.csv")
    prediction_y_path = os.path.join(scores_dir, "prediction_y.csv")
    prediction_real_y_path = os.path.join(scores_dir, "prediction_real_y.csv")
    summary_path = os.path.join(scores_dir, "summary.csv")
    scores.to_csv(scores_path, index=False)
    pd.DataFrame(data=training_y, columns=['Bugged']).to_csv(training_y_path, index=False)
    pd.DataFrame(data=testing_X, columns=training_df.columns).to_csv(testing_x_path, index=False)
    pd.DataFrame(data=testing_y, columns=['Bugged']).to_csv(testing_y_path, index=False)
    columns = list(map(lambda x: str(x), models_info))
    pd.DataFrame(data=np.array(predictions).transpose(), columns=columns).to_csv(prediction_y_path, index=False)
    predictions.append(testing_y)
    columns.append("real")
    pd.DataFrame(data=np.array(predictions).transpose(), columns=columns).to_csv(prediction_real_y_path, index=False)
    summary.to_csv(summary_path, index=False)


class CreateLoggers:
    def __init__(self):
        self._get_loggers()
        self._set_loggers_level()
        self._create_formatters()
        self._create_handlers()
        self._set_formatters_to_handlers()
        self._set_handlers_levels()
        self._set_handlers_to_loggers()

    def _get_loggers(self):
        self.general_log = logging.getLogger(__name__)
        self.summary_log = logging.getLogger('summary')
        self.success_log = logging.getLogger('success')
        self.failure_log = logging.getLogger('failure')
        self.failure_verbose_log = logging.getLogger('failure_verbose')

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
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(5)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(5)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(5)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(5)_failure_verbose.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.summary_file.setFormatter(self.file_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)
        self.failure_verbose_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.summary_file.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)
        self.failure_verbose_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.summary_log.addHandler(self.summary_file)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)
        self.failure_verbose_log.addHandler(self.console)
        self.failure_verbose_log.addHandler(self.failure_verbose_file)


def do(project):
    extract_datasets(project)
    execute(project)


if __name__ == "__main__":
    CreateLoggers()
    projects = [list(ProjectName)[0]]
    projects = list(filter(lambda x: x not in done, projects))
    with Pool(1) as p:
        p.map(do, projects)

