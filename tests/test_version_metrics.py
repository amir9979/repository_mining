import os
import tempfile

import pytest

from git.repo.base import Repo

from config import Config
from metrics.version_metrics import VersionMetrics


def run_before():
    config = Config().config
    jira_project_name = config['TEST_0']['JiraProjectName']
    tests_path = os.path.join("tests", config['TEST_0']['LocalPathName'])
    project_path = Config.get_work_dir_path(tests_path)
    version_name = config['TEST_0']['VersionName']
    github_name = config['TEST_0']['GithubName']
    version_metrics = VersionMetrics(jira_project_name, github_name, project_path, version_name)
    return version_metrics


class TestVersionMetrics:

    # @pytest.mark.skip(reason="takes too long")
    def test_methods_per_file(self):
        version = run_before()
        version.methods_per_file()
        assert False

    @pytest.mark.skip(reason="not working")
    def test_checkstyle_data(self):
        version = run_before()
        version.checkstyle_data()
        assert len(version.checkstyle) != 0

    @pytest.mark.skipif(os.name != "nt")
    def test_source_monitor_data(self):
        version = run_before()
        version.source_monitor_data()
        assert len(version.source_monitor) != 0

    def test_designite_classes(self):
        version = run_before()
        version.designite_data()
        assert len(version.designite_classes) != 0

    def test__designite_helper(self):
        version = run_before()
        assert False

    def test__designite_smells_helper(self):
        version = run_before()
        assert False

    def test_get_closest_id(self):
        version = run_before()
        assert False

    def test_ck_data(self):
        version = run_before()
        assert False

    def test_mood_data(self):
        version = run_before()
        assert False

    def test_halstead_data(self):
        version = run_before()
        assert False
