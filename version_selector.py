import os
import re
import json
from abc import ABC, abstractmethod
from itertools import product
import pandas as pd
from config import Config
from enum import Enum


class VersionType(Enum):
    Major = 1
    Minor = 2
    Micro = 3
    Untyped = 4


class Version():
    def __init__(self, version, version_type, major=0, minor=0, micro=0):
        self.version = version
        self.version_type = version_type
        self.major = major
        self.minor = minor
        self.micro = micro

    def is_untyped(self):
        return self.version_type != VersionType.Untyped

    def is_micro(self):
        return not self.is_untyped()

    def is_minor(self):
        return self.version_type in [VersionType.Minor, VersionType.Major]

    def is_major(self):
        return self.version_type == VersionType.Major


class AbstractSelectVersions(ABC):
    def __init__(self, repo, tags, versions, version_num, version_type, strict=True):
        self.repo = repo
        self.tags = tags
        self.versions = versions
        self.version_num = version_num
        self.versions_by_type = []
        self.versions_selected = []
        self.type = version_type
        self.strict = strict

    def select(self):
        self._get_versions_by_type(self.versions)
        self.tags = list(filter(lambda x: x.version in self.versions_by_type, self.tags))
        self.versions_selected = self._select_versions(self.repo, self.versions_by_type, self.tags)
        self._store_versions(self.repo)
        return self.versions_selected

    @staticmethod
    def define_version_type(version):
        separators = [r'\.', r'\-', r'\_']
        template_base = [['([0-9])', '([0-9])([0-9])', '([0-9])$'], ['([0-9])', '([0-9])([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])([0-9])$'], ['([0-9])([0-9])', '([0-9])$'],
                         ['([0-9])', '([0-9])', '([0-9])$'], ['([0-9])', '([0-9])$']]
        templates = []
        for base in template_base:
            templates.extend(list(map(lambda sep: sep.join(base), separators)))
        templates.extend(['([0-9])([0-9])([0-9])$', '([0-9])([0-9])$'])
        for template in templates:
            values = re.findall(template, version._name)
            if values:
                values = list(map(int, values[0]))
                if len(values) == 4:
                    major, minor1, minor2, micro = values
                    minor = 10 * minor1 + minor2
                elif len(values) == 3:
                    major, minor, micro = values
                else:
                    major, minor = values
                    micro = 0
                if micro != 0:
                    return Version(version, VersionType.Micro, major, minor, micro)
                elif minor != 0:
                    return Version(version, VersionType.Minor, major, minor)
                elif major != 0:
                    return Version(version, VersionType.Major, major)
                else:
                    return Version(version, VersionType.Untyped)
        return Version(version, VersionType.Untyped)

    def _get_versions_by_type(self, versions):
        self.versions_by_type = AbstractSelectVersions.get_versions_by_type(self.type, versions)

    @staticmethod
    def get_versions_by_type(v_type, versions):
        if v_type == VersionType.Untyped:
            return versions
        typed_versions = list(map(AbstractSelectVersions.define_version_type, versions))
        if v_type == VersionType.Major:
            return list(map(lambda x: x.version, filter(Version.is_major, typed_versions)))
        elif v_type == VersionType.Minor:
            return list(map(lambda x: x.version, filter(Version.is_minor, typed_versions)))
        elif v_type == VersionType.Micro:
            return list(map(lambda x: x.version, filter(Version.is_micro, typed_versions)))


    @abstractmethod
    def _select_versions(self, repo, versions_by_type, tags):
        pass

    @abstractmethod
    def _store_versions(versions, repo):
        pass


class BinSelectVersion(AbstractSelectVersions):
    def __init__(self, repo, tags, versions, version_num, version_type, strict, start=(1, 5, 10, 20, 30, 40), step=(5, 10, 20), selected_config=0):
        super().__init__(repo, tags, versions, version_num, version_type, strict)
        self.start = start
        self.step = step
        self.selected_config = selected_config
        self.selected_versions = list()

    def _select_versions(self, repo, versions_by_type, tags):
        relevant_tags = list(filter(lambda t: t.bugged_ratio, tags))
        version_names = list(map(lambda x: x.version._name, relevant_tags))
        only_version = []
        for start, step in product(self.start, self.step):
            bins = list(map(lambda x: list(), range(start, 101, step)))
            for tag in relevant_tags:
                if 100.0 * tag.bugged_ratio < start:
                    continue
                bins[int((100.0 * tag.bugged_ratio - start) / step)].append(tag.version._name)
            for bin_ in bins:
                if len(bin_) < self.version_num:
                    continue
                selected_versions = list(bin_)
                if self.strict:
                    for i in range(len(selected_versions) - self.version_num):
                        versions = tuple(selected_versions[i: i + self.version_num])
                        configuration = {'start': start, 'step': step, 'versions': versions}
                        if len(configuration['versions']) > 1 and configuration['versions'] not in only_version:
                            self.selected_versions.append(configuration)
                            only_version.append(configuration['versions'])
                else:
                    configuration = {'start': start, 'step': step, 'versions': tuple(selected_versions)}
                    if len(configuration['versions']) > 1 and configuration['versions'] not in only_version:
                        self.selected_versions.append(configuration)
                        only_version.append(configuration['versions'])
        self.selected_versions = sorted(self.selected_versions, key=lambda v: sum(map(version_names.index, v['versions'])), reverse=True)
        if len(self.selected_versions) <= self.selected_config:
            print("no versions found")
            exit(0)
        return self.selected_versions[self.selected_config]['versions']

    def _store_versions(self, repo):
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        selected_versions = config["DATA_EXTRACTION"]["SelectedVersionsBin"]
        json_short_data = list()
        ind = 0
        for configuration in self.selected_versions:
            values = list(product([configuration['start']], [configuration['step']],
                                  configuration['versions']))
            name = Config.get_short_name(configuration['versions'])
            columns = ["start", "step", "version"]
            df = pd.DataFrame(values, dtype=str, columns=columns)
            dir_path = os.path.join(repository_data, selected_versions, repo.project.github_name)
            dir_path = Config.get_work_dir_path(dir_path)
            Config.assert_dir_exists(dir_path)
            path = os.path.join(dir_path, str(name) + ".csv")
            df.to_csv(path, index=False, sep=';')
            if len(configuration['versions']) >= 3:
                json_short_data.append({"ind": ind, "name": name, "versions": configuration['versions'], "configuration": configuration})
                ind = ind + 1
        dir_path = os.path.join(repository_data, selected_versions)
        out_path = os.path.join(Config.get_work_dir_path(dir_path), repo.project.github_name + ".json")
        with open(out_path, "w") as f:
            json.dump(json_short_data, f)
        df_dict = list(json_short_data)
        list(map(lambda x: x.pop('configuration'), df_dict))
        pd.DataFrame(df_dict).to_csv(os.path.join(Config.get_work_dir_path(dir_path), repo.project.github_name + ".csv"), index=False, sep=';')



class QuadraticSelectVersion(AbstractSelectVersions):
    def __init__(self, repo, tags, versions, version_num, version_type, strict, min_ratio=0.10, max_ratio=0.30, min_num_commits=100):
        super().__init__(repo, tags, versions, version_num, version_type, strict)
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.min_num_commits = min_num_commits

    def _select_versions(self, repo, versions_by_type, tags):

        def cond1(x, ratio): return x.bugged_ratio <= ratio
        def cond2(x, ratio): return x.bugged_ratio >= ratio
        def cond3(x, num_commits): return x.num_commits >= num_commits
        def conds(x, max_ratio, min_ratio, num_commits): return all([cond1(x, max_ratio), cond2(x, min_ratio), cond3(x, num_commits)])
        max_ratio, min_ratio = self.max_ratio, self.min_ratio
        min_num_commits = self.min_num_commits
        filtered_tags = []
        while len(filtered_tags) < self.version_num:
            if min_num_commits <= 0:
                raise self.NotEnoughVersions("Error: lower the num of versions.")

            filtered_tags = list(filter(lambda tag: conds(tag, max_ratio, min_ratio, min_num_commits) , tags))

            max_ratio += self.max_ratio / 10
            min_num_commits -= self.min_num_commits / 10

        if (not self.strict) or (self.strict and len(filtered_tags) >= self.version_num):
            self.versions_selected = list(map(lambda x: x.version._name, filtered_tags[:self.version_num+1]))
            return

        # The #commits formula is f(x) = 100*x, f(x) > 0 and x > 0
        # The quadratic formula is:
        # f(x) = -100(x-0.2)^2+1, 0 <= f(x) <= 1 and 0.10 <= x <= 0.30

        min_num_commits = 100.00 * float(min(filtered_tags, key=lambda x: x.num_commits).num_commits)
        max_num_commits = 100.00 * float(max(filtered_tags, key=lambda x: x.num_commits).num_commits)
        def num_commits(x): return 100.0 * float(x.num_commits)

        commits_scores = list(map(lambda x: (num_commits(x) - min_num_commits)/(max_num_commits - min_num_commits),
                                  filtered_tags))
        ratio_scores = list(map(lambda x: (-100 * (x.bugged_ratio - 0.2)**2 + 1), filtered_tags))

        values = list(map(lambda x, y, z: (x, str(y + z)), filtered_tags, commits_scores, ratio_scores))
        values.sort(reverse=True, key=lambda x: x[1])
        selected = list(map(lambda x: x[0].version._name, values[:5]))
        self.versions_selected = selected

    class NotEnoughVersions(Exception):
        pass

    def _store_versions(self, repo):
        columns = ["version"]
        values = self.versions_selected
        df = pd.DataFrame(values, columns=columns)
        config = Config().config
        repository_data = config["CACHING"]["RepositoryData"]
        selected_versions = config["DATA_EXTRACTION"]["SelectedVersionsQuadratic"]
        dir_path = os.path.join(repository_data, selected_versions)
        dir_path = Config.get_work_dir_path(dir_path)
        Config.assert_dir_exists(dir_path)
        path = os.path.join(dir_path, repo.project.github_name + ".csv")
        df.to_csv(path, index=False, sep=';')
        pass


class ConfigurationSelectVersion(AbstractSelectVersions):
    def __init__(self, repo, tags, versions, version_num, version_type):
        super().__init__(repo, tags, versions, version_num, version_type)
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
                id = "{0}_{1}_{2}_{3}_{4}_{5}".format(repo.project.github_name, start, stop, step, versions[0], ind)
                versions_dict[id] = repr(tuple(bin)).replace("'", "")

        self.selected_versions = versions_dict

    def _store_versions(self, repo):
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
                                                      PRODUCT_NAME=repo.project.github_name,
                                                      GIT_PATH=repo.project.path,
                                                      VERSIONS=self.selected_versions[id_]))
		
