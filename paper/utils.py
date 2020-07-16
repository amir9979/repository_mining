import itertools
import logging
from functools import partial

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV


class EstimatorSelectionHelper:
    def __init__(self, models, params):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: {0}".format(missing_params))
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {}
        self.general_log = logging.getLogger(__name__)

    def fit(self, X, y, cv=10, n_jobs=1, verbose=1, scoring=None, refit=False):
        for key in self.keys:
            self.general_log.info("Running GridSearchCV for {0}".format(key))
            model = self.models[key]
            params = self.params[key]
            gs = GridSearchCV(model, params, cv=cv, n_jobs=n_jobs, verbose=verbose,
                              scoring=scoring, refit=refit, return_train_score=True)
            gs.fit(X, y)
            self.grid_searches[key] = gs

    def score_summary(self, sort_by='mean_score'):

        def extract_rows(key: str):
            def get_cv_results(cv, params):
                key = "split{}_test_score".format(cv)
                return grid_search.cv_results_[key].reshape(len(params), 1)

            def row(key, scores, params):
                d = {
                    'estimator': key,
                    'min_score': min(scores),
                    'max_score': max(scores),
                    'mean_score': np.mean(scores),
                    'std_score': np.std(scores)
                }
                return pd.Series({**params, **d})

            grid_search = self.grid_searches[key]
            params = grid_search.cv_results_['params']
            get_cv_results_with_params = partial(get_cv_results, params=params)
            scores = np.hstack(list(map(get_cv_results_with_params, range(grid_search.cv))))
            summary = list(map(lambda values: row(key, values[1], values[0]), list(zip(params, scores))))
            return summary

        rows = list(itertools.chain.from_iterable(map(extract_rows, self.grid_searches.keys())))
        df = pd.concat(rows, axis=1).T.sort_values([sort_by], ascending=False)
        columns = ['estimator', 'min_score', 'mean_score', 'max_score', 'std_score']
        columns = columns + [c for c in df.columns if c not in columns]
        return df[columns]

    @staticmethod
    def get_scores_info():
        return ['min_score',
                'max_score',
                'mean_score',
                'std_score']


class FeatureSelectionHelper:
    def __init__(self, methods, features):
        self.methods = methods
        self.selected_features = {}
        self.selected_data = {}
        self.features = features

    def select(self, X, y):
        for method_name, method in self.methods.items():
            self.selected_data[method_name] = method.fit_transform(X, y)
            features_mask = method.get_support()
            self.selected_features[method_name] = np.array(self.features)[features_mask].tolist()
        self.selected_data['all'] = X
        self.selected_features['all'] = list(self.features)

    def get_selected_features(self):
        return self.selected_features

    def get_selected_dataset(self):
        return self.selected_data
