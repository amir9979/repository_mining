import os

from numpy import mean, std
from scipy import stats
from tabulate import tabulate

import pandas as pd
from config import Config


class Hypothesis:
    def __init__(self, h0, h1, prefix, suffix, p1, p2, data1, data2, alpha=0.05):
        self.h0 = h0
        self.h1 = h1
        self.prefix = prefix
        self.suffix = suffix
        self.p1 = p1
        self.p2 = p2
        self.data1 = data1
        self.data2 = data2
        self.count1 = str(len(data1))
        self.count2 = str(len(data2))
        self.mean1 = str(mean(data1))
        self.mean2 = str(mean(data2))
        self.std1 = str(std(data1))
        self.std2 = str(std(data2))

        self.alpha = alpha
        self.t, self.p = stats.ttest_ind(data1, data2)

    def divide(self):
        return self.Color.BLUE + "#" * 100 + "\n"

    def __str__(self):
        output = self.divide()
        output += "\n"
        output += self.Color.GREEN + "H0: " + self.Color.END + \
                  self.prefix + self.Color.RED + ' ' + self.h0 + ' ' + self.Color.END + self.suffix + "\n"
        output += self.Color.BLUE + "H1: " + self.Color.END + \
                  self.prefix + self.Color.RED + ' ' + self.h1 + ' ' + self.Color.END + self.suffix + "\n"
        output += "\n"
        table = [
            [self.Color.YELLOW + self.p1 + self.Color.END,
             self.Color.YELLOW + str(self.count1) + self.Color.END,
             self.Color.YELLOW + self.mean1 + self.Color.END,
             self.Color.YELLOW + self.std1 + self.Color.END],
            [self.Color.PURPLE + self.p2 + self.Color.END,
             self.Color.PURPLE + str(self.count2) + self.Color.END,
             self.Color.PURPLE + self.mean2 + self.Color.END,
             self.Color.PURPLE + self.std2 + self.Color.END]
        ]
        headers = [
            self.Color.DARKCYAN + "Parameter" + self.Color.END,
            self.Color.DARKCYAN + "Count" + self.Color.END,
            self.Color.DARKCYAN + "Mean" + self.Color.END,
            self.Color.DARKCYAN + "Std Dev" + self.Color.END
        ]
        output += tabulate(table, headers=headers)
        output += "\n"
        output += "\n"
        table = [
            [self.Color.DARKCYAN + "t-statistic" + self.Color.END, self.Color.DARKCYAN + str(self.t) + self.Color.END],
            [self.Color.BLUE + "significance" + self.Color.END,
             self.Color.BLUE + str(self.alpha) + self.Color.END],
            [self.Color.DARKCYAN + "p-value" + self.Color.END, self.Color.DARKCYAN + str(self.p) + self.Color.END],
            [self.Color.BLUE + "p-value/2" + self.Color.END, self.Color.BLUE + str(self.p / 2) + self.Color.END]
        ]
        output += tabulate(table) + "\n"
        output += "\n"
        if self.t > 0:
            if self.p / 2 < self.alpha:
                output += self.Color.GREEN + self.Color.BOLD + "Null Hypothesis Rejected " + self.Color.END + "with a {}% confidence.".format(
                        (1 - self.alpha) * 100) + "\n"
                output += self.Color.GREEN + "t > 0\np/2 < alpha" + self.Color.END
            else:
                output += self.Color.RED + self.Color.BOLD + "Null Hypothesis Accepted. " + self.Color.END + "\n"
                output += self.Color.GREEN + "t > 0\n " + self.Color.RED + "p/2 > alpha" + self.Color.END + "\n"
        else:
            if self.p / 2 < self.alpha:
                output += self.Color.RED + self.Color.BOLD + "Null Hypothesis Accepted. " + self.Color.END + "\n"
                output += self.Color.RED + "t <= 0\n " + self.Color.GREEN + "p/2 < alpha" + self.Color.END + "\n"
            else:
                output += self.Color.RED + self.Color.BOLD + "Null Hypothesis Accepted. " + self.Color.END + "\n"
                output += self.Color.RED + "t <= 0\np/2 > alpha" + self.Color.END + "\n"
        output += "\n"
        return output

    class Color:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'


if __name__ == "__main__":
    h0 = "lower or equal"
    h1 = "higher"
    prefix = "Models trained with designite and fowler smells combined produce"
    suffix = "f1-scores than models trained with only fowler smells."

    path = Config.get_work_dir_path(os.path.join("paper", "graphics", "scores", "data.csv"))
    df = pd.read_csv(path, sep=';')

    cond = df['dataset'] == "Designite + Fowler"
    designite_fowler = df.loc[cond]['f1_measure_max']

    cond = df['dataset'] == 'Fowler'
    fowler = df.loc[cond]['f1_measure_max']

    h = Hypothesis(h0, h1, prefix, suffix, "Designite + Fowler", "Fowler", designite_fowler, fowler)
    print(h)
