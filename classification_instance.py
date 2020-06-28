from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class ClassificationInstance(object):
    def __init__(self, training, testing, names, training_path, testing_path, prediction_path):
        self.training = training
        self.training_y = self.training.pop('Bugged').values
        self.training_X = self.training.values
        self.testing = testing
        self.testing_y = self.testing.pop('Bugged').values
        self.testing_X = self.testing.values
        self.names = names.values.tolist()
        self.training.to_csv(training_path, index=False)
        self.testing.to_csv(testing_path, index=False)
        self.prediction_path = prediction_path


    def predict(self):
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        model = classifier.fit(self.training_X, self.training_y)
        prediction = pd.DataFrame(zip(self.names, self.testing_y.to_list(), classifier.predict_proba(self.testing_X)), columns=['name', 'actual', 'faulty_probability'])
        prediction.to_csv(self.prediction_path, index=False)
        return prediction
