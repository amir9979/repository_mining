from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os


class ClassificationInstance(object):
    def __init__(self, training, testing, names, dataset_dir=None, training_path="training.csv", testing_path="testing.csv",
                 training_describe_path="training_describe.csv", testing_describe_path="testing_describe.csv", prediction_path="prediction.csv", label='Bugged', save_all=True):
        self.training = training
        self.testing = testing

        if save_all:
            self.training.to_csv(os.path.join(dataset_dir, training_path), index=False, sep=';')
            self.testing.to_csv(os.path.join(dataset_dir, testing_path), index=False, sep=';')

            self.training.describe(include = 'all').to_csv(os.path.join(dataset_dir, training_describe_path), sep=';')
            self.testing.describe(include = 'all').to_csv(os.path.join(dataset_dir, testing_describe_path), sep=';')
        self.prediction_path = os.path.join(dataset_dir, prediction_path)

        self.training_y = self.training.pop(label).values
        self.training_X = self.training.values
        self.testing_y =None
        if label in self.testing.columns:
            self.testing_y = self.testing.pop(label).values
        self.testing_X = self.testing.values
        self.names = names

    def predict(self):
        classifier = RandomForestClassifier(n_estimators=1000, random_state=42)
        model = classifier.fit(self.training_X, self.training_y)
        classes = list(map(lambda x: str(x) + "_probability", classifier.classes_.tolist()))
        predictions = list(zip(*classifier.predict_proba(self.testing_X)))
        if self.testing_y is not None:
            columns = ['name', 'actual'] + classes
            data = zip(self.names, self.testing_y.tolist(), *predictions)
        else:
            columns = ['name'] + classes
            data = zip(self.names, *predictions)
        prediction = pd.DataFrame(data, columns=columns)
        if self.prediction_path:
            prediction.to_csv(self.prediction_path, index=False, sep=';')
        return prediction

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
        ClassificationInstance(training, testing, methods_testing_names, data_dir, label="BuggedMethods", save_all=save_all).predict()

