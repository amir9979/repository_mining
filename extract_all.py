from Main import Main
from projects import ProjectName
from version_selector import VersionType


def extract_all():
    for n in map(lambda x: x.name, ProjectName):
        m = Main()
        m.set_project_enum(n)
        m.choose_versions(version_num=3, algorithm='bin',
                             version_type=VersionType["Untyped"], strict=False)
        m.set_version_selection(version_num=3, algorithm='bin',
                                   version_type=VersionType["Untyped"], strict=False,
                                selected_config=0)
        m.extract()


if __name__ == '__main__':
    extract_all()