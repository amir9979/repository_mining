import jira
import github3
import os
import csv
import sys
from collections import Counter
from versions import get_repo_versions, get_tags_by_name
from fixing_issues import save_bugs, get_bugged_files_between_versions
from caching import REPOSIROTY_DATA_DIR, cached, assert_dir_exists
from repo import Repo

REPO_DIR = r"C:\Temp\apache_repos"
VERSIONS = os.path.join(REPOSIROTY_DATA_DIR, r"apache_versions")
CONFIGRATION_PATH = os.path.join(REPOSIROTY_DATA_DIR, r"configurations")
assert_dir_exists(CONFIGRATION_PATH)
assert_dir_exists(VERSIONS)
CONFIGRATION = r"""workingDir=C:\amirelm\projects\{WORKING_DIR}
git={GIT_PATH}
issue_tracker_product_name={PRODUCT_NAME}
issue_tracker_url=https://issues.apache.org/jira
issue_tracker=jira
vers={VERSIONS}
"""

def find_repo_and_jira(key, repos, jira_projects):
    jira_project = filter(lambda p: key in [p.key.strip().lower(), "-".join(p.name.strip().lower().split())], jira_projects)[0]
    github = filter(lambda repo: repo.as_dict()['name'].strip().lower() == key, repos)[0]
    return Repo(jira_project.key, github.repository.as_dict()['name'])

@cached("apache_repos_data")
def get_apache_repos_data():
    gh = github3.login('DebuggerIssuesReport', password='DebuggerIssuesReport1') # DebuggerIssuesReport@mail.com
    repos = list(gh.search_repositories('user:apache language:Java'))
    github_repos = map(lambda repo: repo.as_dict()['name'].strip().lower(), repos)
    conn = jira.JIRA(r"http://issues.apache.org/jira")
    jira_projects = conn.projects()
    jira_keys = map(lambda p: p.key.strip().lower(), jira_projects)
    jira_names = map(lambda p: "-".join(p.name.strip().lower().split()), jira_projects)
    jira_elements = list(set(jira_names + jira_keys))
    jira_and_github = map(lambda x: x[0], filter(lambda x: x[1] > 1, Counter(github_repos + jira_elements).most_common()))
    return map(lambda key: find_repo_and_jira(key, repos, jira_projects), jira_and_github)


def search_for_pom(repo):
    for _, _, files in os.walk(repo.local_path):
        if any(map(lambda f: 'pom.xml' in f.lower(), files)):
            return True
        elif any(map(lambda f: 'build.xml' in f.lower(), files)):
            return False
        elif any(map(lambda f: 'gradle' in f.lower(), files)):
            return False
    return False


def sava_bugs_for_project(repo):
    versions = get_repo_versions(repo.local_path)
    if len(versions) < 5:
        return
    save_bugs(os.path.join(VERSIONS, repo.jira_key) + ".csv", repo.local_path, r"http://issues.apache.org/jira", repo.jira_key, versions)


def create_apache_data():
    for repo in get_apache_repos_data():
        sava_bugs_for_project(repo)


def get_versions_by_type(repo):
    import re
    all_versions = get_repo_versions(repo)
    majors = []
    minors = []
    micros = []
    SEPERATORS = ['\.', '\-', '\_']
    template_base = [['([0-9])', '([0-9])([0-9])', '([0-9])$'], ['([0-9])', '([0-9])([0-9])$'], ['([0-9])', '([0-9])', '([0-9])([0-9])$'], ['([0-9])([0-9])', '([0-9])$'], ['([0-9])', '([0-9])', '([0-9])$'], ['([0-9])', '([0-9])$']]
    templates = []
    for base in template_base:
        templates.extend(map(lambda sep: sep.join(base), SEPERATORS))
    templates.extend(['([0-9])([0-9])([0-9])$', '([0-9])([0-9])$'])
    for version in all_versions:
        for template in templates:
            values = re.findall(template, version._name)
            if values:
                values = map(int, values[0])
                if len(values) == 4:
                    micros.append(version)
                    major, minor1, minor2, micro = values
                    minor = 10 * minor1 + minor2
                elif len(values) == 3:
                    micros.append(version)
                    major, minor, micro = values
                else:
                    major, minor = values
                    micro = 0
                if micro == 0:
                    minors.append(version)
                if minor == 0 and micro == 0:
                    majors.append(version)
                break
    return {"all": all_versions, "majors": majors, "minors": minors, "micros": micros}.items()


def choose_versions(repo):
    from itertools import product
    for start, stop, step, versions in product([1, 5, 10], [100], [5, 10, 20], get_versions_by_type(repo.local_path)):
        bins = map(lambda x: list(), range(start, stop, step))
        tags = get_bugged_files_between_versions(repo.local_path, r"http://issues.apache.org/jira", repo.jira_key, versions[1])
        for tag in tags:
            bugged_flies = len(filter(lambda x: "java" in x, tag.bugged_files))
            java_files = len(filter(lambda x: "java" in x, tag.commited_files))
            if bugged_flies*java_files == 0:
                continue
            bugged_ratio = 1.0 * bugged_flies / java_files
            bins[int(((bugged_ratio * 100) - start)/step) - 1].append(tag.tag._name)
        for ind, bin in enumerate(bins):
            if len(bin) < 5:
                continue
            id = "{0}_{1}_{2}_{3}_{4}_{5}".format(repo.jira_key, start, stop, step, versions[0], ind)
            with open(os.path.join(CONFIGRATION_PATH, id), "wb") as f:
                f.write(CONFIGRATION.format(WORKING_DIR=id, PRODUCT_NAME=repo.jira_key, GIT_PATH=repo.local_path, VERSIONS=repr(tuple(bin)).replace("'", "")))


if __name__ == "__main__":
    # print "\n".join(map(lambda x: "{0}, {1}".format(x[0], x[1]), map(lambda x: (
    # os.path.normpath(os.path.join(r'https://github.com/apache', os.path.basename(x[0]))),
    # os.path.normpath(os.path.join(r"http://issues.apache.org/jira/projects", x[1]))), repos)))
    if len(sys.argv) == 3:
        repo, jira_key = sys.argv[1:]
        sava_bugs_for_project(repo, jira_key)
        choose_versions(repo, jira_key)
    else:
        for repo in filter(search_for_pom, get_apache_repos_data()):
            print repo.jira_key
            if repo.jira_key in ["BCEL", "EXEC", "OCM", "POSTAGE", "SCXML", "MNG", "KNOX", "GERONIMODEVTOOLS", "MSCMPUB", "HDFS", "VFS", "HUPA", "CAMEL", "DL", "MINDEXER", "RAMPART", "FUNCTOR", "VELTOOLS", "FILEUPLOAD", "CRUNCH", "JACOB", "JOHNZON", "JOSHUA", "MARMOTTA", "QPID", "MNEMONIC", "TRANSPORTS", "JDKIM", "MPATCH", "DBCP", "CRYPTO", "JEXL", "CURATOR", "WAGON", "MJLINK", "WEAVER", "QPIDJMS", "PULSAR", "DIRECTMEMORY", "NIFI", "EMAIL", "OPENWIRE", "MJAVADOC", "DIRMINA", "JUNEAU", "MRESOLVER", "OAK", "VALIDATOR", "JSPF", "TILES", "MDEP", "ZOOKEEPER", "AIRAVATA", "MRAR", "ROCKETMQ", "OPENEJB", "SUBMARINE", "STANBOL", "NIFIREG", "MRRESOURCES", "HADOOP", "OPENJPA", "SYNCOPE", "SM", "OMID", "MACR", "TEPHRA", "TRINIDAD", "JENA", "LOGGING", "MPDF", "ARCHETYPE", "HAMA", "MRM", "POOL", "PLC4X", "OLTU", "FTPSERVER", "CLOUDSTACK", "MVERIFIER", "METRON", "WICKET", "ARIES", "ACCUMULO", "MSHADE", "UNOMI", "MGPG", "MTOOLCHAINS", "MJDEPRSCAN", "FLINK", "LANG", "MAHOUT", "METAMODEL", "EAGLE", "MPH", "TIKA", "AMBARI", "VXQUERY", "MJDEPS", "RNG", "HELIX", "TINKERPOP", "ISIS", "SYNAPSE", "HCATALOG", "ASTERIXDB", "PROXY", "SAND", "SHINDIG", "IMAGING", "OWB", "MPLUGINTESTING", "TOMEE", "AMQCLI", "GERONIMO", "MLINKCHECK", "JUDDI", "MPIR", "ODFTOOLKIT", "MCHANGELOG", "BVAL", "CAY", "CHAINSAW", "FEDIZ", "BEANUTILS", "OGNL", "TAJO", "CXF", "JSIEVE", "PHOENIX", "PIVOT", "MRESOURCES", "GORA", "IO", "AMQ", "MJAR", "COLLECTIONS", "CONNECTORS", "GRIFFIN", "CHUKWA", "OODT", "KALUMET", "TEZ", "MEJB", "DELTASPIKE", "JELLY", "JCLOUDS", "RANGER", "MEAR", "ARTEMIS", "SENTRY", "APLO", "RYA", "CODEC", "DDLUTILS", "TEXT", "GIRAPH", "BIGTOP", "CONFIGURATION", "MIME4J", "MSITE", "OPENNLP", "STORM", "MDOAP", "MCHANGES", "DOXIA", "ZEPPELIN", "SUREFIRE", "MYFACESTEST", "TWILL", "CONTINUUM", "MCLEAN", "KYLIN", "DOXIATOOLS", "JSEC", "MDEPLOY", "AUTOTAG", "SSHD", "MCOMPILER", "MINSTALL", "SANSELAN", "AVRO", "COMPRESS", "HADOOP", "SHIRO", "EMPIREDB", "BSF", "CMIS", "DIGESTER", "DIRSTUDIO", "FALCON", "NET", "TOBAGO", "MASSEMBLY", "SAVAN", "MINVOKER", "PDFBOX", "JXR", "REEF", "MCHECKSTYLE", "MWAR", "MJMOD", "DBUTILS", "LENS", "ABDERA", "MSTAGE", "MSOURCES", "ATLAS", "HIVE", "MPLUGIN", "ODE", "CXFXJC", "NUMBERS", "BOOKKEEPER", "OPENMEETINGS", "KARAF", "DOXIASITETOOLS", "DRILL", "MPMD", "SIS", "TREQ", "CHAIN", "SYSTEMML", "IGNITE", "CSV", "HBASE", "MANTRUN", "USERGRID", "JXPATH", "COCOON", "WOOKIE", "SCM", "JCI", "JCS", "FLUME", "NUVEM", "DUBBO", "OOZIE", "JCRVLT", "CTAKES", "CLEREZZA", "STREAMS", "CLI", "FELIX", "MATH", "MYFACES", "JSPWIKI", "SMXCOMP"]:
                continue
            try:
                import gc
                gc.collect()
                sava_bugs_for_project(repo)
                choose_versions(repo)
            except:
                raise



