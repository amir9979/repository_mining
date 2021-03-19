import os
import pathlib
import sys
from git import Repo
from Main import Main


# LOCATION_PROJECT = "C:/Users/shir0/camel"
NAME_PROJECT = "camel"


def write_commit(list_of_commit):
    if not os.path.exists('apache_repos'):
        os.mkdir('apache_repos')
        os.mkdir('apache_repos/' + NAME_PROJECT)
        Repo.init('apache_repos/' + NAME_PROJECT)
        
    if len(list_of_commit) == 0:
        exit()
    for commit in list_of_commit:
        all_file_of_commit = commit.stats.files
        list_file_that_change = find_java_file(all_file_of_commit)
        for file_change in list_file_that_change:
            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs:
                    if diff.new_file or diff.deleted_file:
                        continue
                    if diff.b_path == file_change:
                        try:
                            file = file_change[file_change.rfind('/') + 1:-5]
                            before_contents = list(map(lambda x: x.decode("utf-8", errors='ignore'),
                                                       diff.a_blob.data_stream.stream.readlines()))
                            after_contents = list(map(lambda x: x.decode("utf-8", errors='ignore'),
                                                      diff.b_blob.data_stream.stream.readlines()))
                            write(before_contents, commit, file, "before")
                            write(after_contents, commit, file)

                        except Exception as e:
                            print("commit ", commit)
                            print(e)
                            pass


def find_java_file(list_of_file):
    list_file = list()
    for file in list_of_file:
        if file.endswith(".java") and not file.endswith("Test.java"):
            list_file.append(file)
    return list_file


def write(contents, commit, file, name="after"):
    if name == "before":
        if not os.path.exists('apache_repos/' + NAME_PROJECT + '/' + str(commit)):
            os.mkdir('apache_repos/' + NAME_PROJECT + '/' + str(commit))
        if not os.path.exists('apache_repos/' + NAME_PROJECT + '/' + str(commit) + "/" + file):
            os.mkdir('apache_repos/' + NAME_PROJECT + '/' + str(commit) + "/" + file)

    with open('apache_repos/' + NAME_PROJECT + '/' + str(
            commit) + "/" + file + "/" + name +
              ".java", 'w') as file:
        for line in contents:
            file.write('%s' % line)


class GetCommit:

    def __init__(self, url, start_index, end_index):
        self.URL = url
        self.connect = Repo(self.URL, search_parent_directories=True)
        assert not self.connect.bare
        self.list_of_commit = self.get_all_commit(start_index, end_index)

    def get_all_commit(self, start_index, end_index):
        list_all_commit = list()
        commits = list(self.connect.iter_commits('master'))
        for commit in commits[start_index:end_index]:
            list_all_commit.append(commit)
        return list_all_commit


if __name__ == '__main__':

    commits_start = int(sys.argv[1]) * 500
    commits_end = commits_start + 500
    obj_git = GetCommit('my-tools', commits_start, commits_end)
    write_commit(obj_git.list_of_commit)
    version_before = 'shir_' + str(commits_start)
    main = Main()
    main.set_project(NAME_PROJECT, "", NAME_PROJECT.upper(), "http://issues.apache.org/jira")
    data_types = ["checkstyle", "halstead", "designite_design", "ck", "designite_implementation"]
    main.extract_features_to_version(version_before, False, data_types=data_types)

