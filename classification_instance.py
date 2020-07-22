from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os


class ClassificationInstance(object):
    def __init__(self, training, testing, names, dataset_dir, training_path="training.csv", testing_path="testing.csv",
                 training_describe_path="training_describe.csv", testing_describe_path="testing_describe.csv", prediction_path="prediction.csv", label='Bugged'):
        self.training = training
        self.testing = testing

        self.training.to_csv(os.path.join(dataset_dir, training_path), index=False)
        self.testing.to_csv(os.path.join(dataset_dir, testing_path), index=False)

        self.training.describe().to_csv(os.path.join(dataset_dir, training_describe_path), index=False)
        self.testing.describe().to_csv(os.path.join(dataset_dir, testing_describe_path), index=False)

        self.training_y = self.training.pop(label).values
        self.training_X = self.training.values
        self.testing_y = self.testing.pop(label).values
        self.testing_X = self.testing.values
        self.names = names
        self.prediction_path = os.path.join(dataset_dir, prediction_path)


    def predict(self):
        classifier = RandomForestClassifier(n_estimators=1000, random_state=42)
        model = classifier.fit(self.training_X, self.training_y)
        prediction = pd.DataFrame(zip(self.names, self.testing_y.tolist(), classifier.predict_proba(self.testing_X)), columns=['name', 'actual', 'faulty_probability'])
        prediction.to_csv(self.prediction_path, index=False)
        return prediction
