import os
import re
from abc import ABC, abstractmethod
from itertools import product

import pandas as pd

from config import Config
from repo import Repo


class AbstractSelectVersions(ABC):
    def __init__(self, repo, tags, versions, version_num=5, type="all"):
        self.repo = repo
        self.tags = tags
        self.versions = versions
        self.version_num = version_num
        self.versions_by_type: list
        self.versions_selected: list
        self.type = all

    def select(self):
        self._get_versions_by_type(self.versions)
        self._select_versions(self.repo, self.versions_by_type, self.tags)
        self._store_versions(self.repo)

    def _get_versions_by_type(self, versions):
        majors, minors, micros = []
        separators = ['\.', '\-', '\_']
        template_base = [['([0-9])', '([0-9])([0-9])', '([0-9])$'], ['([0-9])', '([0-9])([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])([0-9])$'], ['([0-9])([0-9])', '([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])$'], ['([0-9])', '([0-9])$']]
        templates = []
        for base in template_base:
            templates.extend(map(lambda sep: sep.join(base), separators))
        templates.extend(['([0-9])([0-9])([0-9])$', '([0-9])([0-9])$'])
        for version in versions:
            for template in templates:
                values = re.findall(template, version._name)
                if values:
                    values = map(int, values[0])
                    if len(values) == 4:
                        micros.append(version)
                        major, minor1, minor2, micro = values
                        minor = 10 * minor1 + minor2
                    elif len(values) == 3:
                        micros.append(version)
                        major, minor, micro = values
                    else:
                        major, minor = values
                        micro = 0
                    if micro == 0:
                        minors.append(version)
                    if minor == 0 and micro == 0:
                        majors.append(version)
                    break

        if self.type == "all":
            self.versions_by_type = versions
        elif self.type == "majors":
            self.versions_by_type = majors
        elif self.type == "minors":
            self.versions_by_type = minors
        elif self.type == "micros":
            self.versions_by_type = micros
        else:
            raise Exception("Error: " + self.type + " not an option.")

    @abstractmethod
    def _select_versions(self, repo, versions_by_type, tags):
        pass

    @abstractmethod
    def _store_versions(versions, repo: Repo):
        pass


class BinSelectVersion(AbstractSelectVersions):
    def __init__(self, repo, tags, versions, version_num=5):
        super().__init__()

    def _select_versions(self, repo, versions_by_type, tags):
        versions = []
        for start, stop, step, versions in product([1, 5, 10], [100], [5, 10, 20],
                                                   self._get_versions_by_type()):
            bins = map(lambda x: list(), range(start, stop, step))
            tags = self._get_bugged_files_between_versions()
            for tag in tags:
                bugged_flies = len(list(filter(lambda x: "java" in x, tag.bugged_files)))
                java_files = len(list(filter(lambda x: "java" in x, tag.version_files)))
                if bugged_flies * java_files == 0:
                    continue
                bugged_ratio = 1.0 * bugged_flies / java_files
                bins[int(((bugged_ratio * 100) - start) / step) - 1].append(tag.version._name)
            for ind, bin in enumerate(bins):
                if len(bin) < self.versions_num:
                    continue
                versions.append(repr(tuple(bin)).replace("'", ""))

        self.selected_versions = versions

    def _store_versions(self, repo: Repo):
        values = [self.selected_versions]
        df = pd.DataFrame(values, columns=["versions"])
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        selected_versions = config["DATA_EXTRACTION"]["SelectedVersions"]
        dir_path = os.path.join(repository_data, selected_versions)
        Config.assert_dir_exists(dir_path)
        path = os.path.join(dir_path, repo.github_name + ".csv")
        df.to_csv(path, index=False)


class QuadraticSelectVersion(AbstractSelectVersions):

    def __init__(self, repo, tags, versions, version_num=5):
        super().__init__(repo, tags, versions, version_num)

    def _select_versions(self, versions_by_type, tags):
        pass

    def _store_versions(versions, repo: Repo):
        pass


class ConfigurationSelectVersion(AbstractSelectVersions):
    def __init__(self, repo, tags, versions, version_num=5):
        super().__init__(repo, tags, versions, version_num)
        self.configuration = r"""workingDir={WORKING_DIR}
            git={GIT_PATH}
            issue_tracker_product_name={PRODUCT_NAME}
            issue_tracker_url=https://issues.apache.org/jira
            issue_tracker=jira
            vers={VERSIONS}
            """

    def _select_versions(self, repo, versions_by_type, tags):
        versions_dict = {}
        for start, stop, step, versions in product([1, 5, 10], [100], [5, 10, 20], self.versions_by_type):
            bins = list(map(lambda x: list(), range(start, stop, step)))
            for tag in tags:
                bugged_files = len(list(filter(lambda x: "java" in x, tag.bugged_files)))
                java_files = len(list(filter(lambda x: "java" in x, tag.version_files)))
                if bugged_files * java_files == 0:
                    continue
                bugged_ratio = 1.0 * bugged_files / java_files
                bins[int(((bugged_ratio * 100) - start) / step) - 1].append(tag.version._name)
            for ind, bin_ in enumerate(bins):
                if len(bin_) < self.versions_num:
                    continue
                id = "{0}_{1}_{2}_{3}_{4}_{5}".format(repo.jira_key, start, stop, step, versions[0], ind)
                versions_dict[id] = repr(tuple(bin)).replace("'", "")

        self.selected_versions = versions_dict

    def _store_versions(self, repo: Repo):
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        configuration_path = config["DATA_EXTRACTION"]["ConfigurationsPaths"]
        configuration_dir = os.path.join(repository_data, configuration_path)
        Config.assert_dir_exists(configuration_dir)
        working_dir = config["DATA_EXTRACTION"]["ConfigurationsWorkingDir"]
        Config.assert_dir_exists(working_dir)
        for id_ in self.selected_versions:
            path = os.path.join(configuration_dir, id_)
            with open(path, "wb") as file_:
                file_.write(self.configuration.format(WORKING_DIR=os.path.join(working_dir, id),
                                                      PRODUCT_NAME=repo.jira_key,
                                                      GIT_PATH=repo.local_path,
                                                      VERSIONS=self.selected_versions[id_]))
