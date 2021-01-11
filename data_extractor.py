import os
from datetime import datetime
from functools import reduce
from pathlib import Path

import git
import json
import pandas as pd

from commit import Commit, CommittedFile
from config import Config
from fixing_issues import VersionInfo
from issues import get_issues_for_project
from version_selector import ConfigurationSelectVersion, BinSelectVersion, QuadraticSelectVersion, VersionType, AbstractSelectVersions
from versions import Version
from caching import cached
from repo import Repo


class DataExtractor(object):

    def __init__(self, project, quick_mode=False):
        self.project = project
        self.quick_mode = quick_mode
        self.github_name = self.project.github_name
        self.repo = Repo(self.project)
        self.git_repo = git.Repo(self.project.path)
        self.head_commit = self.git_repo.head.commit.hexsha
        # self.git_repo.git.checkout(self.head_commit, force=True)
        self.git_url = os.path.join(list(self.git_repo.remotes[0].urls)[0].replace(".git", ""), "tree")
        self.issues = None
        self.commits = None
        self.versions = None
        self.bugged_files_between_versions = None
        self.selected_config = self.read_selected_config()
        self.selected_versions = None
        self.get_selected_versions()

    def set_selected_config(self, val):
        self.selected_config = val
        out_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'],
                         Config().config['DATA_EXTRACTION']['SelectedVersionsInd']))
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(out_dir, self.github_name), "w") as f:
            json.dump({"selected_config": self.selected_config}, f)
        self.get_selected_versions(force=True)

    def read_selected_config(self):
        out_dir = Config.get_work_dir_path(
            os.path.join(Config().config['CACHING']['RepositoryData'],
                         Config().config['DATA_EXTRACTION']['SelectedVersionsInd']))
        path = os.path.join(out_dir, self.github_name)
        if not os.path.exists(path):
            return 0
        with open(path) as f:
            return int(json.loads(f.read())["selected_config"])

    def checkout_version(self, version):
        self.git_repo.git.checkout(version.replace('\\', '/'), force=True)

    def checkout_master(self):
        self.git_repo.git.checkout(self.head_commit, force=True)

    @staticmethod
    def _get_repo_commits(repo, jira_issues):
        issues = dict(map(lambda x: (x.issue_id, x), jira_issues))
        commits = DataExtractor._commits_and_issues(repo, issues)
        return commits

    @staticmethod
    def _get_repo_versions(repo):
        repo_tags = sorted(list(repo.tags), key=lambda t: t.commit.committed_date)
        tags = zip(list(repo_tags)[1:], list(repo_tags))
        versions = list(map(lambda tag: Version(tag[0], DataExtractor._version_files(tag[0], tag[1])),
                            tags))
        return sorted(versions, key=lambda version: version._commit._commit_date)

    def _get_bugged_files_between_versions(self, versions, analyze_methods=False):
        tags_commits = self._get_commits_between_versions(versions)
        tags = []
        analyze_methods = analyze_methods if not self.quick_mode else False
        for tag in tags_commits:
            if tags_commits[tag]:
                tags.append(VersionInfo(tag, tags_commits[tag], self.git_repo, analyze_methods=analyze_methods))
            else:
                print("not commits for", tag._name)
        return sorted(tags, key=lambda x: x.version._commit._commit_date)

    def init_jira_commits(self):
        # self.issues = get_jira_issues(self.project.jira_name, self.jira_url)
        self.issues = get_issues_for_project(self.project)
        self.commits = self._get_repo_commits(self.git_repo, self.issues)
        self.versions = self._get_repo_versions(self.git_repo)
        print("number of commits: ", len(self.commits))
        print("number of tags: ", len(self.versions))
        self.bugged_files_between_versions = self._get_bugged_files_between_versions(self.versions)

    def extract(self, selected_versions=False):
        tags = self.bugged_files_between_versions
        self._store_issues()
        self._store_commited_files()
        self._store_commits()
        self._store_versions(tags, False)
        self._store_versions_infos(tags)
        self._store_files(tags)
        if selected_versions:
            tags = self._get_bugged_files_between_versions(list(filter(lambda tag: tag._name in list(map(lambda x: os.path.normpath(str(x)), self.get_selected_versions())), self.versions)), True)
            self._store_versions(tags, True)
            self._store_versions_infos(tags, True)
            self._store_files(tags, True)
            if not self.quick_mode:
                self._store_methods(tags)

    def _store_issues(self):
        def clean(s):
            return "".join(list(filter(lambda c: c.isalpha(), s)))

        # TO DO: fix it to save to jira and bz
        df = pd.DataFrame(list(map(lambda x: x.fields, self.issues)), columns=self.issues[0].fields.keys())
        commited_files_dir = self._get_caching_path("Issues")
        path = os.path.join(commited_files_dir, self.github_name + ".csv")
        df.to_csv(path, index=False, sep=';')
        issues_df = pd.DataFrame(list(map(lambda x: x.to_features_dict(), self.issues)))
        to_dummies = ['priority', 'resolution', 'type']
        dummies_dict = {}
        for d in to_dummies:
            dummies = pd.get_dummies(issues_df[d], prefix=d)
            dummies = dummies.rename(columns={c: clean(c) for c in dummies.columns.to_list()})
            dummies_dict[d] = dummies.columns.tolist()
            issues_df = pd.concat([issues_df, dummies], axis=1)
            issues_df.drop([d], axis=1, inplace=True)

        dummies_path = os.path.join(commited_files_dir, self.github_name + "_dummies.csv")
        issues_df.to_csv(dummies_path, index=False, sep=';')

    def _store_commited_files(self):
        columns = ["file_name", "insertions", "deletions", "changes", 'is_java', "commit_id", "issue_id", "commit_date", "commit_url", "bug_url"]
        commited_files = list(map(lambda c:
                                  list(map(lambda f:
                                           [f.name, f.insertions, f.deletions, f.insertions + f.deletions, f.is_java, c._commit_id,
                                            c._issue_id, c._commit_formatted_date, self.get_commit_url(c._commit_id), c.get_issue_url()],
                                           c._files)), self.commits))

        commited_files = reduce(list.__add__, commited_files, [])
        df = pd.DataFrame(commited_files, columns=columns)
        commited_files_dir = self._get_caching_path("CommittedFiles")
        path = os.path.join(commited_files_dir, self.github_name + ".csv")
        df.to_csv(path, index=False, sep=';')

    def _store_commits(self):
        columns = ["commit_id", 'is_java', "issue_id", "commit_date", "commit_url", "bug_url"]
        commits = list(map(lambda c: [c._commit_id, c.is_java_commit, c._issue_id, c._commit_formatted_date, self.get_commit_url(c._commit_id), c.get_issue_url()], self.commits))
        df = pd.DataFrame(commits, columns=columns)
        commits_dir = self._get_caching_path("Commits")
        path = os.path.join(commits_dir, self.github_name + ".csv")
        df.to_csv(path, index=False, sep=';')

    def _store_versions(self, tags, selected=False):
        columns = ["version_name", "#commited_files_in_version", "#bugged_files_in_version", "bugged_ratio",
                   "#commits", "#bugged_commits", "#ratio_bugged_commits", "version_date", "version_url", "version_type"]
        df = pd.DataFrame(columns=columns)
        for tag in tags:
            version = {"version_name": tag.version._name,
                       "#commited_files_in_version": len(tag.version_files),
                       "#bugged_files_in_version": len(tag.bugged_files),
                       "bugged_ratio": tag.bugged_ratio,
                       "#commits": tag.num_commits,
                       "#bugged_commits": tag.num_bugged_commits,
                       "#ratio_bugged_commits": tag.ratio_bugged_commits,
                       "version_date": tag.version._commit._commit_formatted_date,
                       "version_url": self.get_commit_url(tag.version._commit._commit_id),
                       "version_type": AbstractSelectVersions.define_version_type(tag.version).version_type.name}
            df = df.append(version, ignore_index=True)
        if selected:
            versions_dir = os.path.join(self._get_caching_path("SelectedVersions"), self.github_name)
            Config.assert_dir_exists(versions_dir)
            path = os.path.join(versions_dir, Config.get_short_name(self.get_selected_versions()) + ".csv")
            df.to_csv(path, index=False, sep=';')
        else:
            versions_dir = self._get_caching_path("AllVersions")
            Config.assert_dir_exists(versions_dir)
            path = os.path.join(versions_dir, self.github_name + ".csv")
            df.to_csv(path, index=False, sep=';')
            versions_dir = self._get_caching_path("Versions")
            Config.assert_dir_exists(versions_dir)
            path = os.path.join(versions_dir, self.github_name + ".csv")
            df[df['version_type'].apply(lambda x: x.lower() in ['minor', 'major'])].to_csv(path, index=False, sep=';')

    def get_commit_url(self, commit_sha):
        return os.path.normpath(os.path.join(self.git_url, commit_sha))

    def get_versions_by_type(self, v_types=(VersionType.Minor, VersionType.Major)):
        versions = []
        for v_type in v_types:
            versions.extend(AbstractSelectVersions.get_versions_by_type(v_type, self.versions))
        return versions

    def _store_versions_infos(self, tags, selected=False):
        if selected:
            versions_infos_dir = os.path.join(self._get_caching_path("SelectedVersionsInfos"), self.github_name, Config.get_short_name(self.get_selected_versions()))
        else:
            versions_infos_dir = os.path.join(self._get_caching_path("VersionsInfos"), self.github_name)
        Config.assert_dir_exists(versions_infos_dir)
        for tag in tags:
            df = pd.DataFrame(tag.commits_shas, columns=["commit_id", "is_buggy"])
            version_name = os.path.normpath(tag.version._name).replace(os.path.sep, "_")
            path = os.path.join(versions_infos_dir, version_name + ".csv")
            df.to_csv(path, index=False, sep=';')

    def _store_methods(self, tags):
        methods_dir = os.path.join(self._get_caching_path("SelectedMethods"), self.github_name,
                                 Config.get_short_name(self.get_selected_versions()))
        Config.assert_dir_exists(methods_dir)
        for tag in tags:
            methods = dict()
            for method in tag.all_methods:
                data = (method.id, method.method_name, method.method_name_parameters, method.file_name, method.start_line, method.end_line, method.changed)
                if method.id in methods:
                    if method.changed:
                        methods[method.id] = data
                else:
                    methods[method.id] = data
            df = pd.DataFrame(methods.values(), columns=["method_id", "method_name", "method_name_parameters", "file_name", "start_line", "end_line", "is_method_buggy"])
            version_name = tag.version._name.replace(os.path.sep, "_")
            path = os.path.join(methods_dir, version_name + ".csv")
            df.to_csv(path, index=False, sep=';')


    def _store_files(self, tags, selected=False):
        if selected:
            files_dir = os.path.join(self._get_caching_path("SelectedFiles"), self.github_name, Config.get_short_name(self.get_selected_versions()))
        else:
            files_dir = os.path.join(self._get_caching_path("Files"), self.github_name)
        Config.assert_dir_exists(files_dir)
        for tag in tags:
            files = {file_name: False for file_name in tag.version_files}
            files.update({file_name: True for file_name in tag.bugged_files})
            df = pd.DataFrame(files.items(), columns=["file_name", "is_buggy"])
            version_name = tag.version._name.replace(os.path.sep, "_")
            path = os.path.join(files_dir, version_name + ".csv")
            df.to_csv(path, index=False, sep=';')

    def _get_commits_between_versions(self, versions):
        sorted_versions = sorted(versions, key=lambda version: version._commit._commit_date)
        sorted_commits_and_versions = sorted(versions + list(filter(lambda x: x.is_java_commit, self.commits)),
                                             key=lambda version: version._commit._commit_date if hasattr(version,
                                                                                                         "_commit") else version._commit_date)
        versions_indices = list(map(lambda version: (version, sorted_commits_and_versions.index(version)), sorted_versions))
        selected_versions = list(filter(lambda vers: vers[0][1] < vers[1][1], zip(versions_indices, versions_indices[1:])))
        return dict(
            map(lambda vers: (vers[0][0], sorted_commits_and_versions[vers[0][1] + 1: vers[1][1]]), selected_versions))

    def _get_caching_path(self, config_name):
        config = Config().config
        file_name = config['DATA_EXTRACTION'][config_name]
        repository_data = config["CACHING"]["RepositoryData"]
        repository_data = Config().get_work_dir_path(repository_data)
        path = os.path.join(repository_data, file_name, self.github_name)
        Config.assert_dir_exists(path)
        return path

    @staticmethod
    def _version_files(new_tag, prev_tag):
        return list(map(lambda diff: diff.b_path, new_tag.commit.tree.diff(prev_tag.commit.tree)))

    @staticmethod
    def _clean_commit_message(commit_message):
        if "git-svn-id" in commit_message:
            return commit_message.split("git-svn-id")[0]
        return commit_message

    @staticmethod
    def _commits_and_issues(repo, issues):
        def replace(chars_to_replace, replacement, s):
            temp_s = s
            for c in chars_to_replace:
                temp_s = temp_s.replace(c, replacement)
            return temp_s

        def get_bug_num_from_comit_text(commit_text, issues_ids):
            text = replace("[]?#,:(){}'\"", "", commit_text.lower())
            text = replace("-_", " ", text)
            text = replace("bug", " ", text)
            text = replace("fix", " ", text)
            for word in text.split():
                if word.isdigit():
                    if word in issues_ids:
                        return word
            return "0"

        commits = []
        java_commits = DataExtractor._get_commits_files(repo)
        for git_commit in java_commits:
            bug_id = "0"
            if all(list(map(lambda x: not x.is_java, java_commits[git_commit]))):
                commit = Commit.init_commit_by_git_commit(git_commit, bug_id, None, java_commits[git_commit], False)
                commits.append(commit)
                continue
            try:
                commit_text = DataExtractor._clean_commit_message(git_commit.summary)
            except:
                continue
            bug_id = get_bug_num_from_comit_text(commit_text, dict(filter(lambda x: x[1].creation_time <= git_commit.committed_datetime, issues.items())))
            commits.append(
                Commit.init_commit_by_git_commit(git_commit, bug_id, issues.get(bug_id), java_commits[git_commit]))
        return commits

    @staticmethod
    def _get_commits_files(repo):
        data = repo.git.log('--numstat','--pretty=format:"sha: %H"').split("sha: ")
        comms = {}
        for d in data[1:]:
            d = d.replace('"', '').replace('\n\n', '\n').split('\n')
            commit_sha = d[0]
            comms[commit_sha] = []
            for x in d[1:-1]:
                insertions, deletions, name = x.split('\t')
                names = Commit.fix_renamed_files([name])
                comms[commit_sha].extend(list(map(lambda n: CommittedFile(commit_sha, n, insertions, deletions), names)))
        return dict(map(lambda x: (repo.commit(x), comms[x]), filter(lambda x: comms[x], comms)))

    def choose_versions(self, repo=None, version_num=5, configurations=False,
                        algorithm="bin", version_type=VersionType.Untyped, strict=True):
        if self.selected_versions is not None:
            return
        tags = self.bugged_files_between_versions
        if repo is None:
            repo = self.repo

        if configurations:
            selector = ConfigurationSelectVersion(repo, tags, self.versions, version_num, version_type)
        else:
            if algorithm == "bin":
                selector = BinSelectVersion(repo, tags, self.versions, version_num, version_type, strict=strict, selected_config=self.selected_config)
            elif algorithm == "quadratic":
                selector = QuadraticSelectVersion(repo, tags, self.versions, version_num, version_type, strict=strict)
            else:
                raise Exception("Error: you picked the wrong algorithm")

        self.selected_versions = selector.select()

    def get_selected_versions(self, force=False):
        if self.selected_versions and not force:
            return self.selected_versions
        repo_data = Config().config['CACHING']['RepositoryData']
        selected = Config().config['DATA_EXTRACTION']['SelectedVersionsBin']
        path = os.path.join(repo_data, selected, self.github_name + ".json")
        in_path = Config.get_work_dir_path(path)
        if os.path.exists(in_path):
            with open(in_path) as f:
                self.selected_versions = list(filter(lambda c: str(c['ind']) == str(self.selected_config), json.loads(f.read())))[0]['versions']
            return self.selected_versions
        return None

    def get_files_bugged(self, version):
        files_dir = self._get_caching_path("Files")
        path = os.path.join(files_dir, version+".csv")
        if os.path.exists(path):
            return pd.read_csv(path, sep=';').to_dict('records')
        versions = list(filter(lambda tag: tag.version._name == version, self.bugged_files_between_versions))
        if (not versions):
            raise Exception("Error: version not found")
        tag = versions[0]
        files = {file_name: False for file_name in tag.version_files}
        files.update({file_name: True for file_name in tag.bugged_files})
        return files

    def get_bugged_files_path(self, version, selected_versions=False):
        if selected_versions:
            cache_path = self._get_caching_path("SelectedFiles")
            path = os.path.join(cache_path, self.github_name, Config.get_short_name(self.get_selected_versions()), version.replace(os.path.sep, "_") + '.csv')
        else:
            cache_path = self._get_caching_path("Files")
            path = os.path.join(cache_path, self.github_name, version.replace(os.path.sep, "_") + '.csv')
        return path

    def get_bugged_methods_path(self, version):
        cache_path = self._get_caching_path("SelectedMethods")
        path = os.path.join(cache_path, self.github_name, Config.get_short_name(self.get_selected_versions()), version.replace(os.path.sep, "_") + '.csv')
        return path


if __name__ == "__main__":
    from projects import ProjectName
    DataExtractor(ProjectName.CommonsLang.value).extract()
