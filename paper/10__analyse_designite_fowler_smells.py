import functools
import logging
import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from config import Config
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataNameEnum
from paper.utils import EstimatorSelectionHelper
from projects import ProjectName

done = []


def build_dataset(version, project):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    try:
        db = DataBuilder(project, version)

        db.append(DataNameEnum.GodClass)
        db.append(DataNameEnum.ClassDataShouldBePrivate)
        db.append(DataNameEnum.ComplexClass)
        db.append(DataNameEnum.LazyClass)
        db.append(DataNameEnum.RefusedBequest)
        db.append(DataNameEnum.SpaghettiCode)
        db.append(DataNameEnum.SpeculativeGenerality)
        db.append(DataNameEnum.DataClass)
        db.append(DataNameEnum.BrainClass)
        db.append(DataNameEnum.LargeClass)
        db.append(DataNameEnum.SwissArmyKnife)
        db.append(DataNameEnum.AntiSingleton)
        db.append(DataNameEnum.FeatureEnvy)
        db.append(DataNameEnum.LongMethod_Organic)
        db.append(DataNameEnum.LongParameterList_Organic)
        db.append(DataNameEnum.MessageChain)
        db.append(DataNameEnum.DispersedCoupling)
        db.append(DataNameEnum.IntensiveCoupling)
        db.append(DataNameEnum.ShotgunSurgery)
        db.append(DataNameEnum.BrainMethod)
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
            raise Exception("Fowler smells dataset is empty.")

        def union_smell(value):
            return any(value)

        aggregation_fns = {feature: union_smell for feature in list(methods_df.columns)[3:]}
        aggregated_methods_df = methods_df.groupby(['File', 'Class']).aggregate(aggregation_fns).reset_index()
        classes_df.dropna(inplace=True)
        dataset = classes_df.merge(aggregated_methods_df, on=['File', 'Class'], how='outer')
        dataset.fillna(False, inplace=True)
        return dataset

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

    dataset_dir = Config.get_work_dir_path(os.path.join("paper", "datasets", "designite_fowler", project.github()))
    Path(dataset_dir).mkdir(parents=True, exist_ok=True)
    training_path = os.path.join(dataset_dir, "training.csv")
    testing_path = os.path.join(dataset_dir, "testing.csv")

    pd.concat(datasets[:-1], ignore_index=True).drop(["File", "Class"], axis=1).to_csv(training_path, index=False)
    datasets[-1].drop(["File", "Class"], axis=1).to_csv(testing_path, index=False)


def execute(project):
    dataset_dir = Config.get_work_dir_path(os.path.join("paper", "datasets", "designite_fowler", project.github()))
    Path(dataset_dir).mkdir(parents=True, exist_ok=True)
    training_path = os.path.join(dataset_dir, "training.csv")
    testing_path = os.path.join(dataset_dir, "testing.csv")

    training_df = pd.read_csv(training_path).dropna().astype(int)
    testing_df = pd.read_csv(testing_path).dropna().astype(int)

    training_y = training_df.pop('Bugged').values
    training_X = training_df.values

    oversample = SMOTE()
    training_X, training_y = oversample.fit_resample(training_X, training_y)

    models = {
        'LinearDiscriminantAnalysis': LinearDiscriminantAnalysis(),
        'QuadraticDiscriminantAnalysis': QuadraticDiscriminantAnalysis(),
        'LogisticRegression': LogisticRegression(),
        'BernoulliNaiveBayes': BernoulliNB(),
        'K-NearestNeighbor': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(),
        'RandomForest': RandomForestClassifier(),
        'SupportVectorMachine': SVC(),
        # 'MultilayerPerceptron': MLPClassifier()
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
        # 'MultilayerPerceptron': {'hidden_layer_sizes': [(17, 8, 17)],
        #                          'activation': ['tanh', 'relu']}
    }

    helper = EstimatorSelectionHelper(models, params)
    helper.fit(training_X, training_y, scoring='f1')
    summary = helper.score_summary()
    top_summary = summary[:10]
    top_summary_iter = top_summary.drop(EstimatorSelectionHelper.get_scores_info(), axis=1)\
                                  .where(pd.notnull(top_summary), None)\
                                  .iterrows()

    testing_y = testing_df.pop('Bugged').values
    testing_X = testing_df.values
    models_info = list(map(lambda x: x[1].to_dict(), top_summary_iter))

    columns = ['estimator', 'configuration', 'precision', 'recall', 'f1-measure', 'auc-roc', 'brier score']
    scores = pd.DataFrame(columns=columns)
    predictions = []
    for model_info in models_info:
        estimator = models[model_info['estimator']]
        params = {key: val for key, val in model_info.items() if not (val is None or key == 'estimator')}
        estimator.set_params(**params)
        estimator.fit(training_X, training_y)
        prediction_y = estimator.predict(testing_X)
        predictions.append(prediction_y)
        scores_dict = {
            'estimator': model_info['estimator'],
            'configuration': str(params),
            'precision': precision_score(testing_y, prediction_y),
            'recall': recall_score(testing_y, prediction_y),
            'f1-measure': f1_score(testing_y, prediction_y),
            'auc-roc': roc_auc_score(testing_y, prediction_y),
            'brier score': brier_score_loss(testing_y, prediction_y)
        }
        scores = scores.append(scores_dict, ignore_index=True)
    scores_dir = Config.get_work_dir_path(os.path.join("paper", "scores", "designite_fowler", project.github()))
    Path(scores_dir).mkdir(parents=True, exist_ok=True)
    scores_path = os.path.join(scores_dir, "scores.csv")
    training_x_path = os.path.join(scores_dir, "training_x.csv")
    training_y_path = os.path.join(scores_dir, "training_y.csv")
    testing_x_path = os.path.join(scores_dir, "testing_x.csv")
    testing_y_path = os.path.join(scores_dir, "testing_y.csv")
    prediction_y_path = os.path.join(scores_dir, "prediction_y.csv")
    prediction_real_y_path = os.path.join(scores_dir, "prediction_real_y.csv")
    summary_path = os.path.join(scores_dir, "summary.csv")
    scores.to_csv(scores_path, index=False)
    pd.DataFrame(data=training_X, columns=training_df.columns).to_csv(training_x_path, index=False)
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
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(10)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(10)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(10)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(10)_failure_verbose.log"), "a")

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
    projects = list(ProjectName)
    projects = list(filter(lambda x: x not in done, projects))
    with Pool() as p:
        p.map(do, projects)
