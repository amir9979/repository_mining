from Main import Main
from projects import ProjectName
from version_selector import VersionType
import sys


def extract_all(repo_path):
    m = Main()
    for proj in ProjectName:
        if proj.value.github_name.lower() in repo_path.lower():
            m.set_project_enum(proj.name)
            break
    m.choose_versions(version_num=3, algorithm='bin',
                         version_type=VersionType["Untyped"], strict=False)
    m.set_version_selection(version_num=3, algorithm='bin',
                               version_type=VersionType["Untyped"], strict=False,
                            selected_config=0)
    m.extract(False)


if __name__ == '__main__':
    extract_all(sys.argv[1])
