from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
import pandas as pd
import json
import os
import sklearn.metrics as metrics


class ClassificationInstance(object):
    def __init__(self, training, testing, names=None, dataset_dir=None, training_path="training.csv", testing_path="testing.csv",
                 training_describe_path="training_describe.csv", testing_describe_path="testing_describe.csv", prediction_path="prediction.csv", label='bugged_Bugged', save_all=True, metrics_path='metrics.json', importance_path='importance.json'):
        self.training = training
        self.testing = testing
        self.save_all = save_all
        if self.save_all:
            self.training.to_csv(os.path.join(dataset_dir, training_path), index=False, sep=';')
            self.testing.to_csv(os.path.join(dataset_dir, testing_path), index=False, sep=';')

            self.training.describe(include = 'all').to_csv(os.path.join(dataset_dir, training_describe_path), sep=';')
            self.testing.describe(include = 'all').to_csv(os.path.join(dataset_dir, testing_describe_path), sep=';')
        self.prediction_path = os.path.join(dataset_dir, prediction_path)
        self.metrics_path = os.path.join(dataset_dir, metrics_path)
        self.importance_path = os.path.join(dataset_dir, importance_path)
        self.scores = None
        self.importance = None
        self.fix_and_warn(label)
        self.training_y = self.training.pop(label).values
        self.features_list = self.training.columns.to_list()
        self.training_X = self.training.values
        self.testing_y = None
        if label in self.testing.columns:
            self.testing_y = self.testing.pop(label).values
        self.testing_X = self.testing.values
        self.names = names

    def fix_and_warn(self, label):
        test_ = set(self.testing.columns.to_list())
        train_ = set(self.training.columns.to_list())
        not_in_test = train_ - test_
        not_in_train = test_ - train_
        if not_in_test:
            print(f"WARN: {not_in_test} columns are not in test")
        if not_in_train:
            print(f"WARN: {not_in_train} columns are not in train")
        all_cols = list(train_.intersection(test_))
        self.training = self.training[all_cols]
        self.testing = self.testing[all_cols]

    def predict(self):
        classifier = RandomForestClassifier(n_estimators=1000, random_state=42)
        # classifier = GaussianProcessClassifier(kernel=RBF(), max_iter_predict=20, n_restarts_optimizer=0, warm_start=True)
        model = classifier.fit(self.training_X, self.training_y)
        classes = list(map(lambda x: str(x) + "_probability", classifier.classes_.tolist()))
        predictions_proba = list(zip(*classifier.predict_proba(self.testing_X)))
        predictions = list(classifier.predict(self.testing_X))
        self.importance = dict(zip(self.features_list, classifier.feature_importances_.tolist()))
        if self.save_all:
            with open(self.importance_path, "w") as f:
                json.dump(self.importance, f)
        if self.names:
            names = self.names
        else:
            names = ['' for _ in self.testing_y.tolist()]
        if self.testing_y is not None:
            columns = ['name', 'actual', 'prediction'] + classes
            data = zip(names, self.testing_y.tolist(), predictions, *predictions_proba)
            self.evaluate_on_test(self.testing_y.tolist(), predictions, classifier.classes_.tolist(), predictions_proba)
        else:
            columns = ['name', 'prediction'] + classes
            data = zip(names, predictions, *predictions_proba)
        prediction = pd.DataFrame(data, columns=columns)
        if self.prediction_path:
            prediction.to_csv(self.prediction_path, index=False, sep=';')
        return prediction

    def evaluate_on_test(self, y_true, y_pred, classes, predicitons_proba):
        self.scores = {}
        y_prob_true = dict(zip(classes, predicitons_proba))[True]
        y_prob_false = dict(zip(classes, predicitons_proba))[False]
        self.scores['accuracy_score'] = metrics.accuracy_score(y_true, y_pred)
        self.scores['precision_score'] = metrics.precision_score(y_true, y_pred)
        self.scores['recall_score'] = metrics.recall_score(y_true, y_pred)
        self.scores['f1_score'] = metrics.f1_score(y_true, y_pred)
        self.scores['roc_auc_score_True'] = metrics.roc_auc_score(y_true, y_prob_true)
        self.scores['roc_auc_score_False'] = metrics.roc_auc_score(y_true, y_prob_false)
        self.scores['pr_auc_score_True'] = pr_auc_score(y_true, y_prob_true)
        self.scores['pr_auc_score_False'] = pr_auc_score(y_true, y_prob_false)
        if self.save_all:
            with open(self.metrics_path, "w") as f:
                json.dump(self.scores, f)

    @staticmethod
    def instance_for_rest_versions(training_path, testing_path, data_dir, save_all=True):
        training = pd.read_csv(training_path, delimiter=";").drop("Method_ids", axis=1, errors='ignore')
        testing = pd.read_csv(testing_path, delimiter=";")
        for col in testing:
            dt = testing[col].dtype
            if dt == int or dt == float:
                testing[col].fillna(0, inplace=True)
            else:
                testing[col].fillna(False, inplace=True)
        methods_testing_names = testing.pop("Method_ids").values.tolist()
        ClassificationInstance(training, testing, methods_testing_names, data_dir, label="bugged_methods_BuggedMethods", save_all=save_all).predict()

    @staticmethod
    def all_but_one_evaluation(dataset_dir):
        for sub_dir, label in [("methods", "bugged_methods_BuggedMethods"), ("classes_no_aggregate", "bugged_Bugged")]:
            scores = []
            for e_type in ('one', 'all'):
                d_dir = os.path.join(dataset_dir, e_type, sub_dir)
                for data_type in os.listdir(d_dir):
                    d_type_dir = os.path.join(d_dir, data_type)
                    training = pd.read_csv(os.path.join(d_type_dir, "training.csv"), delimiter=';').drop("Method_ids", axis=1, errors='ignore')
                    testing = pd.read_csv(os.path.join(d_type_dir, "testing.csv"), delimiter=";")
                    for col in testing:
                        dt = testing[col].dtype
                        if dt == int or dt == float:
                            testing[col].fillna(0, inplace=True)
                        else:
                            testing[col].fillna(False, inplace=True)
                    ci = ClassificationInstance(training, testing, None, d_type_dir, label=label, save_all=True)
                    try:
                        ci.predict()
                        ci_scores = dict(ci.scores)
                        ci_scores.update({"type": e_type, "data_type": data_type})
                        scores.append(ci_scores)
                    except Exception as e:
                        print(e)
                        pass
            pd.DataFrame(scores).to_csv(os.path.join(dataset_dir, sub_dir + "_metrics.csv"), index=False, sep=';')


def pr_auc_score(y_true, y_score):
    precision, recall, thresholds =  metrics.precision_recall_curve(y_true, y_score)
    return metrics.auc(recall, precision)


if __name__ == "__main__":
    ClassificationInstance.all_but_one_evaluation(r"C:\Users\User\Downloads\dataset\commons-lang")
