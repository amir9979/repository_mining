import os
import pandas as pd
from pathlib import Path

from classification_instance import ClassificationInstance
from metrics.version_metrics_name import DataNameEnum


class Compare:
    def __init__(self, name, groupA_name, groupB_name, groupA, groupB):
        self.name = name
        self.groupA_name = groupA_name
        self.groupB_name = groupB_name
        self.groupA = groupA
        self.groupB = groupB
        self.groupA_features = []
        self.groupB_features = []
        for d in DataNameEnum:
            data_type = d.value.data_type.value
            if data_type in self.groupA:
                self.groupA_features.append(d.value.name)
            if data_type in self.groupB:
                self.groupB_features.append(d.value.name)

    def create_compare_datasets(self, origin_dataset):
        training_df = pd.read_csv(os.path.join(origin_dataset, "training.csv"), sep=';')
        testing_df = pd.read_csv(os.path.join(origin_dataset, "testing.csv"), sep=';')
        names = pd.read_csv(os.path.join(origin_dataset, "prediction.csv"), sep=';')['name'].to_list()
        dataset_cols = set(training_df.columns.to_list()).intersection(set(testing_df.columns.to_list()))
        ans = self.create_sub_data_set_by_columns({self.groupA_name: self.groupA_features, self.groupB_name: self.groupB_features}, dataset_cols, self.name, "bugged_Bugged", names, '',
                                                  testing_df, training_df, origin_dataset)
        pd.DataFrame(ans).to_csv(os.path.join(os.path.dirname(origin_dataset), self.name + ".csv"), index=False, sep=';')


    def create_sub_data_set_by_columns(self, columns, dataset_cols, dir_name, label, names, sub_dir, testing_df,
                                       training_df, origin_dataset):
        scores = []
        for d in columns:
            cols = set(filter(lambda dc: any(map(lambda c: c in dc, columns[d])), dataset_cols))
            if len(cols) == 0:
                continue
            cols.add(label)
            cols = list(cols)
            train = training_df[cols]
            test = testing_df[cols]
            dataset_dir = os.path.join(os.path.dirname(origin_dataset), dir_name, sub_dir, d)
            Path(dataset_dir).mkdir(parents=True, exist_ok=True)
            ci = ClassificationInstance(train, test, names, dataset_dir,
                                        label=label)
            try:
                ci.predict()
                ci_scores = dict(ci.scores)
                ci_scores.update({"type": dir_name, "data_type": d})
                scores.append(ci_scores)
            except Exception as e:
                print(e)
        return scores


def results_analysis():
    base = r"C:\Temp\fer"
    dirs = list(
        filter(lambda x: os.path.isdir(x[1]), map(lambda x: (x, os.path.join(base, x, 'dataset')), os.listdir(base))))

    product_compare = Compare("product_compare", "traditional_product", "issues_product", ["halstead", "jasome_files", "jasome_mood", "jasome_ck", "jasome_lk"], ["issues_product"])
    process_compare = Compare("process_compare", "traditional_process", "issues_process", ["process_files"], ["issues_process"])
    for d in dirs:
        classes_dir = os.path.join(d[1], os.listdir(d[1])[0], 'classes')
        product_compare.create_compare_datasets(classes_dir)
        process_compare.create_compare_datasets(classes_dir)

if __name__ == "__main__":

    results_analysis()