import re
import time


class Commit(object):
    def __init__(self, bug_id, git_commit):
        # self._git_commit = git_commit
        self._commit_id = git_commit.hexsha
        self._bug_id = bug_id
        self._files = Commit.fix_renamed_files(git_commit.stats.files.keys())
        self._commit_date = time.mktime(git_commit.committed_datetime.timetuple())
        # self._git_commit = git_commit

    def is_bug(self):
        return self._bug_id != '0'

    @classmethod
    def init_commit_by_git_commit(cls, git_commit, bug_id):
        return Commit(bug_id, git_commit)

    def to_list(self):
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]

    @staticmethod
    def fix_renamed_files(files):
        """
        fix the paths of renamed files.
        before : u'tika-core/src/test/resources/{org/apache/tika/fork => test-documents}/embedded_with_npe.xml'
        after:
        u'tika-core/src/test/resources/org/apache/tika/fork/embedded_with_npe.xml'
        u'tika-core/src/test/resources/test-documents/embedded_with_npe.xml'
        :param files: self._files
        :return: list of modified files in commit
        """
        new_files = []
        for file in files:
            if "=>" in file:
                if "{" and "}" in file:
                    # file moved
                    src, dst = file.split("{")[1].split("}")[0].split("=>")
                    fix = lambda repl: re.sub(r"{[\.a-zA-Z_/\-0-9]* => [\.a-zA-Z_/\-0-9]*}", repl.strip(), file)
                    new_files.extend(map(fix, [src, dst]))
                else:
                    # full path changed
                    new_files.extend(map(lambda x: x.strip(), file.split("=>")))
                    pass
            else:
                new_files.append(file)
        return new_files
