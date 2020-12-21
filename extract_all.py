from Main import Main
from projects import ProjectName
from version_selector import VersionType
import sys


def extract_all(name):
    m = Main()
    m.set_project_enum(name)
    m.choose_versions(version_num=3, algorithm='bin',
                         version_type=VersionType["Untyped"], strict=False)
    m.set_version_selection(version_num=3, algorithm='bin',
                               version_type=VersionType["Untyped"], strict=False,
                            selected_config=0)
    m.extract()


if __name__ == '__main__':
    extract_all(sys.argv[1])