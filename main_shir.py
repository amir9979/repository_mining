import os
import pathlib
import pickle
import sys
from git import Repo
from Main import Main
from commit import Commit

# LOCATION_PROJECT = "C:/Users/shir0/camel"
NAME_PROJECT = "camel"


def extract_files_commits(obj_git):
    data = obj_git.connect.git.log('--numstat', '--name-status', '--pretty=format:"sha: %H parents: %P"').split("sha: ")
    comms = {}
    files = {}
    for d in data[1:]:
        d = d.replace('"', '').replace('\n\n', '\n').split('\n')
        sha, parent = d[0].split(" parents: ")
        commit_sha = sha
        comms[commit_sha] = [parent.split(" "), []]
        for x in d[1:-1]:
            try:
                split = x.split('\t')
                status, name = split[0], split[1:]
                if len(name) == 1:
                    name = name[0]
                if status.startswith("R"):
                    if name[0].endswith(".java") and not name[0].endswith("Test.java"):
                        if len(parent.split(" ")) > 1:
                            print(f"{name[0]}")
                        name = Commit.fix_renamed_files(name)
                        comms[commit_sha][1].extend([name])
                        # files.setdefault(name, []).append(commit_sha)
                elif name.endswith(".java") and not name.endswith("Test.java"):
                    if status != 'A' and status != "D":
                        if len(parent.split(" ")) > 1:
                            print(f"{name}")
                        name = Commit.fix_renamed_files([name])[0]
                        comms[commit_sha][1].extend([name])
                        # files.setdefault(name, []).append(commit_sha)
            except Exception as e:
                print(e)
                print(x)
                pass
    return dict(map(lambda x: (x, comms[x]), filter(lambda x: comms[x][1], comms))), files


def write_commit(list_of_commit, commits_start, commits_end):
    if not os.path.exists('apache_repos'):
        os.mkdir('apache_repos')
        os.mkdir('apache_repos/' + NAME_PROJECT)
        Repo.init('apache_repos/' + NAME_PROJECT)

    if len(list_of_commit) == 0:
        exit()
    for commit in list(list_of_commit.keys())[commits_start:commits_end]:
        all_file_of_commit = list_of_commit[commit][1]
        for file_change in all_file_of_commit:
            # if len(list_of_commit[commit][0]) > 1:
            #     print("commit ", commit)
            #     print("parent ", list_of_commit[commit][0])
            #     print("file_change ", file_change)
            for parent in list_of_commit[commit][0]:
                # TODO more than one parents
                try:
                    if type(file_change) is list:
                        file_before_rename = file_change[0]
                        file_after_rename = file_change[1]
                        file = file_after_rename[file_after_rename.rfind('/') + 1:-5]
                        after_contents = obj_git.connect.git.show('{}:{}'.format(commit, file_after_rename))
                        before_contents = obj_git.connect.git.show('{}:{}'.format(parent, file_before_rename))
                    else:
                        file = file_change[file_change.rfind('/') + 1:-5]
                        after_contents = obj_git.connect.git.show('{}:{}'.format(commit, file_change))
                        before_contents = obj_git.connect.git.show('{}:{}'.format(parent, file_change))
                    write(before_contents, commit, file, "before")
                    write(after_contents, commit, file)
                except Exception as e:
                    print("commit ", commit)
                    print("parent ", parent)
                    print("file_change ", file_change)
                    # obj_git.connect.git.log('--follow', file_change)
                    print(e)
                    pass


def write(contents, commit, file, name="after"):
    if name == "before":
        if not os.path.exists('apache_repos/' + NAME_PROJECT + '/' + str(commit)):
            os.mkdir('apache_repos/' + NAME_PROJECT + '/' + str(commit))
        if not os.path.exists('apache_repos/' + NAME_PROJECT + '/' + str(commit) + "/" + file):
            os.mkdir('apache_repos/' + NAME_PROJECT + '/' + str(commit) + "/" + file)

    with open('apache_repos/' + NAME_PROJECT + '/' + str(
            commit) + "/" + file + "/" + name +
              ".java", 'w') as file:
        file.write(''.join(contents))


class GetCommit:

    def __init__(self, url, start_index, end_index):
        self.URL = url
        self.connect = Repo(self.URL, search_parent_directories=True)
        assert not self.connect.bare
        # self.list_of_commit = self.get_all_commit(start_index, end_index)

    def get_all_commit(self, start_index, end_index):
        list_all_commit = list()
        commits = list(self.connect.iter_commits('master'))
        for commit in commits[start_index:end_index]:
            list_all_commit.append(commit)
        return list_all_commit


if __name__ == '__main__':
    window_ind = int(sys.argv[1])
    window_size = int(sys.argv[2])
    commits_start = window_ind * window_size
    commits_end = commits_start + window_size
    obj_git = GetCommit('my-tools', commits_start, commits_end)
    commits, files = extract_files_commits(obj_git)
    write_commit(commits, commits_start, commits_end)
    version_before = 'shir_' + str(commits_start)
    main = Main()
    main.set_project(NAME_PROJECT, "", NAME_PROJECT.upper(), "http://issues.apache.org/jira")
    data_types = ["checkstyle", "halstead", "designite_design", "ck", "designite_implementation", "jasome_mood", "jasome_ck", "jasome_lk", "jasome_files"]
    main.extract_features_to_version(version_before, False, data_types=data_types)
