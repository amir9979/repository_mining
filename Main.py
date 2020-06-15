import argparse
from projects import ProjectName, Project
from data_extractor import DataExtractor

class Main():
    def list_projects(self):
        print("\n".join(list(map(lambda e: "{0}: {1}".format(e.name, e.value.description()), ProjectName))))

    def extract(self, project):
        DataExtractor(project)

    def get_project(self, github, jira):
        return Project(github, jira)

    def main(self):
        parser = argparse.ArgumentParser(description='Execute project data')
        parser.add_argument('-p', '--projects', dest='projects', action='store_const', const=True, default=False,
                            help='list all aleready defined projects')
        parser.add_argument('-c', '--choose', dest='choose', action='store', help='choose a project to extract')
        parser.add_argument('-g', '--github_url', dest='github', action='store', help='the git link to the project to extract')
        parser.add_argument('-j', '--jira_url', dest='jira', action='store', help='the jira link to the project to extract')
        parser.add_argument('-s', '--select_verions', dest='select', action='store', help='the algorithm to select the versions : [bin, quadratic]', default='bin')
        parser.add_argument('-n', '--num_verions', dest='num_versions', action='store', help='the the number of versions to select', default=5, type=int)
        args = parser.parse_args()
        if args.projects:
            self.list_projects()
        if args.choose:
            self.extract(ProjectName[args.choose])
        if args.github and args.jira:
            self.extract(self.get_project(args.github, args.jira))


if __name__ == "__main__":
    Main().main()