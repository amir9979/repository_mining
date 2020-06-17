import logging
import sys
from multiprocessing import Pool

import functools
import os

sys.path.append("..")
from config import Config
from metrics.version_metrics import Bugged, Checkstyle, Designite, CK, Halstead
from projects import ProjectName


def extract_metrics(version, project):
    general_log = logging.getLogger(__name__)
    success_log = logging.getLogger("success")
    failure_log = logging.getLogger("failure")
    failure_verbose_log = logging.getLogger("failure_verbose")

    try:
        general_log.info("{0}:{1} analyzing files...".format(
            project.github(),
            version))

        extractors = {
            # "Bugged": Bugged(project, version),
            "Checkstyle": Checkstyle(project, version),
            # "Designite": Designite(project, version),
            # "Ck": CK(project, version),
            # "Halstead": Halstead(project, version)
            # TODO fix "Mood": Mood(project, version),
        }
    except Exception:
        failure_log.error("{0} | {1}:{2} failed to analyze files".format(
            "_".join([project.github(), version, "analyze"]).lower(),
            project.github(),
            version))
        failure_verbose_log.exception("{0} | {1}:{2} failed to analyze files".format(
            "_".join([project.github(), version, "analyze"]).lower(),
            project.github(),
            version))
        return False

    succeeded = True
    for extractor_name, extractor in extractors.items():
        try:
            general_log.info("{0}:{1} extracting {2}...".format(
                project.github(),
                version,
                extractor_name
            ))
            extractor.extract()
            success_log.info("{0}:{1} succeeded to extract {2}".format(
                project.github(),
                version,
                extractor_name))

        except Exception:
            general_log.info("{0}:{1} failed to extract {2}\n".format(
                project.github(),
                version,
                extractor_name))

            failure_log.error("{0} | {1}:{2} failed to extract {3}".format(
                "_".join([project.github(), version, extractor_name]).lower(),
                project.github(),
                version,
                extractor_name))

            failure_verbose_log.exception("{0} | {1}:{2} failed to extract {3}".format(
                "_".join([project.github(), version, extractor_name]).lower(),
                project.github(),
                version,
                extractor_name))

            succeeded = False
    return succeeded


def execute(project_tuple):
    general_log = logging.getLogger(__name__)
    summary_log = logging.getLogger('summary')

    index = project_tuple[0]
    project = project_tuple[1][0]
    versions = project_tuple[1][1]
    general_log.info("extracting {0}:{1}".format(index, project))

    versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
    versions_path = os.path.join(versions_dir, project.github() + ".csv")
    # versions = pd.read_csv(versions_path)['version'].to_list()
    extract = functools.partial(extract_metrics,
                                project=project)
    success_summary = list(map(extract, versions))
    if all(success_summary):
        summary_log.info("Project {0} succeeded.".format(project.github()))
    else:
        summary_log.info("Project {0} failed.".format(project.github()))


class CreateLoggers:
    def __init__(self):
        self._get_loggers()
        self._set_loggers_level()
        self._create_formatters()
        self._create_handlers()
        self._set_formatters_to_handlers()
        self._set_handlers_levels()
        self._set_handlers_to_loggers()

    def _get_loggers(self):
        self.general_log = logging.getLogger(__name__)
        self.summary_log = logging.getLogger('summary')
        self.success_log = logging.getLogger('success')
        self.failure_log = logging.getLogger('failure')
        self.failure_verbose_log = logging.getLogger('failure_verbose')

    def _set_loggers_level(self):
        self.general_log.setLevel(logging.INFO)
        self.summary_log.setLevel(logging.INFO)
        self.success_log.setLevel(logging.INFO)
        self.failure_log.setLevel(logging.ERROR)
        self.failure_verbose_log.setLevel(logging.ERROR)

    def _create_formatters(self):
        self.console_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(message)s'
        )

        self.file_formatter = logging.Formatter(
            '%(asctime)s | %(message)s'
        )

    def _create_handlers(self):
        self.console = logging.StreamHandler()
        paper_dir = Config.get_work_dir_path(os.path.join("paper", "logs"))
        self.summary_file = logging.FileHandler(os.path.join(paper_dir, "(4)_summary.log"), "a")
        self.success_file = logging.FileHandler(os.path.join(paper_dir, "(4)_success.log"), "a")
        self.failure_file = logging.FileHandler(os.path.join(paper_dir, "(4)_failure.log"), "a")
        self.failure_verbose_file = logging.FileHandler(os.path.join(paper_dir, "(4)_failure_verbose.log"), "a")

    def _set_formatters_to_handlers(self):
        self.console.setFormatter(self.console_formatter)
        self.summary_file.setFormatter(self.file_formatter)
        self.success_file.setFormatter(self.file_formatter)
        self.failure_file.setFormatter(self.file_formatter)
        self.failure_verbose_file.setFormatter(self.file_formatter)

    def _set_handlers_levels(self):
        self.console.setLevel(logging.INFO)
        self.summary_file.setLevel(logging.INFO)
        self.success_file.setLevel(logging.INFO)
        self.failure_file.setLevel(logging.ERROR)
        self.failure_verbose_file.setLevel(logging.ERROR)

    def _set_handlers_to_loggers(self):
        self.general_log.addHandler(self.console)
        self.summary_log.addHandler(self.summary_file)
        self.success_log.addHandler(self.console)
        self.success_log.addHandler(self.success_file)
        self.failure_log.addHandler(self.console)
        self.failure_log.addHandler(self.failure_file)
        self.failure_verbose_log.addHandler(self.console)
        self.failure_verbose_log.addHandler(self.failure_verbose_file)


if __name__ == "__main__":
    CreateLoggers()

    projects = [
        # (ProjectName.ActiveMQ, ["activemq-5.8.0", "activemq-5.3.0", "activemq-5.9.0"]),
        # (ProjectName.Airavata, ["airavata-0.16", "airavata-0.14", "airavata-0.11"]),
        # (ProjectName.Archiva, ["archiva-1.4-M3", "archiva-1.2-M1", "archiva-1.4-M2", "archiva-1.3", "archiva-1.2.2",  "archiva-1.3.5"]),
        # (ProjectName.AsterixDB, ["asterix-0.8.7-incubating", "fullstack-0.2.9", "apache-hyracks-0.3.1", "asterix-0.0.5", "asterix-0.8.3", "asterix-0.8.5"]),
        # (ProjectName.Avro, ["release-1.9.1-rc3", "release-1.9.0-rc4", "release-1.8.1-rc1", "release-1.8.0", "release-1.8.2-rc1"]),
        # (ProjectName.Camel, ["camel-1.6.0", "camel-2.0-M1", "camel-1.6.1"]),
        # (ProjectName.Cassandra, ["cassandra-0.6.1", "cassandra-0.6.5", "cassandra-0.6.4"]),
        # (ProjectName.Cayenne, ["4.0.M4", "4.0.M2", "4.0.M5", "4.1.B2", "4.0", "4.0.B1"]),
        # (ProjectName.CommonsCLI, ["cli-1.2-RC7", "cli-1.1-RC3"]),
        # (ProjectName.CommonsJexl, ["COMMONS_JEXL_3_1", "COMMONS_JEXL_2_0_1-RC3", "COMMONS_JEXL-1_1-RC1", "v4.0-snapshot.3"]),
        # (ProjectName.CommonsMath, ["MATH_3_2", "MATH_2_2", "MATH_3_0", "MATH_3_3", "MATH_3_0_RC3"]),
        # (ProjectName.CommonsValidator, ["VALIDATOR_1_5_1", "VALIDATOR_1_5_0"]),
        # (ProjectName.CXF, ["cxf-2.1.1", "cxf-2.1.3", "cxf-2.1.2"]),
        # (ProjectName.DirectoryServer, ["1.5.7", "2.0.0-M24", "1.5.4", "2.0.0-M19", "1.5.5"]),
        # (ProjectName.DirectoryStudio, ["2.0.0.v20130628", "1.5.2.v20091211", "2.0.0.v20180908-M14"]),
        # (ProjectName.Flink, ["release-0.8.1", "release-0.7.0", "release-1.0.3", "release-1.3.2-rc3", "release-0.9.0"]),
        # (ProjectName.Giraph, ["release-1.0.0-RC3", "release-0.1.0"]),
        # (ProjectName.Groovy, ["GROOVY_2_4_7", "GROOVY_2_2_1", "GROOVY_2_4_6", "GROOVY_1_6_3"]),
        # (ProjectName.Hadoop, ["release-2.2.0", "release-2.1.1-beta-rc0", "release-2.1.0-beta", "release-0.23.10"]),
        # (ProjectName.Helix, ["helix-0.6.1-incubating", "helix-0.6.3", "helix-0.8.0"]),
        # (ProjectName.Isis, ["rel/isis-1.12.2", "interim/isis-1.16.0.20180130-1145", "interim/isis-1.15.1.20171221-1739", "rel/isis-1.7.0", "interim/isis-1.16.1.20180316-1549", "interim/isis-1.15.1.20171028-1842", "interim/isis-1.15.1.20171220-1335"]),
        # (ProjectName.Jackrabbit, ["1.5.5", "2.0-alpha3", "1.3.1", "2.0.0", "2.0-alpha2"]),
        # (ProjectName.JClouds, ["jclouds-1.6.0-rc.1", "jclouds-1.5.2", "jclouds-1.5.4", "jclouds-1.5.0-alpha.6", "jclouds-1.5.5"]),
        # (ProjectName.Jena, ["jena-3.13.1", "jena-3.2.0-rc1", "jena-3.9.0-rc1", "jena-3.14.0", "jena-3.12.0"]),
        # (ProjectName.Johnzon, ["v1.1.12", "v0.9.3-incubating", "v1.1.4", "v0.8-incubating", "v0.9.1-incubating"]),
        # (ProjectName.Juneau, ["juneau-7.2.0-RC2", "juneau-8.1.2-RC1", "juneau-8.0.0-RC1"]),
        # (ProjectName.Karaf, ["karaf-2.1.2"]),
        # (ProjectName.Knox, ["v0.2.0-branch", "v1.3.0-rc2", "v0.6.0-release", "v1.1.0-release", "v1.0.0-release"]),
        # (ProjectName.Lucene, ["releases/lucene-solr/4.10.4", "releases/lucene/3.0.0"]),
        # (ProjectName.ManifoldCF, ["release-2.13", "release-1.3", "release-1.2", "release-1.1.1", "release-2.0.2"]),
        # (ProjectName.Maven, ["maven-3.5.0-alpha-1", "maven-3.0-alpha-5", "maven-3.0.1"]),
        # (ProjectName.Nifi, ["rel/nifi-1.4.0", "rel/nifi-0.7.0", "rel/nifi-1.9.2", "rel/nifi-0.6.1"]),
        # (ProjectName.Nutch, ["release-1.15", "release-1.13", "release-1.12"]),
        # (ProjectName.Ofbiz, ["REL-13.07.01", "REL-10.04.02", "REL-12.04.01"]),
        # (ProjectName.OpenJPA, ["2.3.0", "1.2.0", "1.0.3"]),
        # (ProjectName.OpenNLP, ["opennlp-1.5.3-rc3", "opennlp-1.7.2", "opennlp-1.6.0-rc6", "opennlp-1.7.1"]),
        # (ProjectName.Phoenix, ["v4.11.0-HBase-0.98-rc1", "v4.7.0-HBase-0.98-rc6"]),
        # (ProjectName.Roller, ["roller-5.2.4-rc-1", "roller-5.2.2", "roller_5.1.2-rc1"]),
        # (ProjectName.Santuario, ["xmlsec-2.1.4", "xmlsec-2.0.6", "xmlsec-2.0.2", "xmlsec-2.0.10"]),
        # (ProjectName.Shiro, ["shiro-root-1.3.2-release-vote1", "shiro-root-1.4.1"]),
        # (ProjectName.Storm, ["v0.9.2-incubating-security", "v0.9.4", "v1.2.3", "v0.9.3", "v1.0.1"]),
        # (ProjectName.Struts, ["STRUTS_2_1_0", "STRUTS_2_1_6", "STRUTS_2_0_8"]),
        # (ProjectName.Tez, ["release-0.5.2", "release-0.5.1-rc0", "release-0.6.0-rc0", "release-0.9.1-rc2", "release-0.5.3-rc1"]),
        # (ProjectName.TinkerPop, ["3.4.2"]),
        # (ProjectName.Tomee, ["tomee-1.5.2", "tomee-1.6.0"]),
        # (ProjectName.UimaRuta, ["ruta-2.6.1", "ruta-2.8.0", "ruta-2.7.0"]),
        # (ProjectName.Wicket, ["wicket-6.8.0", "rel/wicket-6.23.0", "wicket-1.3.0-beta3", "wicket-1.5.7", "wicket-7.0.0-M2"]),
        # (ProjectName.FOP, ["fop-1_1", "RELEASE_0_12_0", "fop-2_2", "fop-0_95", "fop-2_3"])
        # ---
        # (ProjectName.ActiveMQArtemis, ["1.2.0", "1.3.0", "1.5.3", "2.4.0", "2.6.3"]),
        # (ProjectName.Beam, ["v2.3.0-RC3", "v2.4.0-RC3", "v2.1.0-RC2", "v2.8.0-RC1", "v2.9.0-RC1"]),
        # (ProjectName.Metron, ["apache-metron-0.3.0-rc1-incubating", "apache-metron-0.4.2-release", "Metron_0.2.1BETA_rc2", "apache-metron-0.5.0-rc2", "apache-metron-0.4.1-release"]),
        # (ProjectName.Plc4x, ["release/0.3.1", "rel/0.1.0", "release/0.2.0", "release/0.6.0", "release/0.3.0"])
        # (ProjectName.Cocoon, ["RELEASE_2_1_5_1", "RELEASE_2_1_1", "RELEASE_2_1_2", "RELEASE_2_1_6", "RELEASE_2_1_3"]),
        # (ProjectName.CarbonData, ["apache-carbondata-1.1.0", "apache-carbondata-1.1.1", "apache-carbondata-1.4.0-rc1",
        #                           "apache-carbondata-1.2.0", "apache-carbondata-2.0.0-rc1"]),
        # (ProjectName.CommonsCSV,
        #  ["rel/commons-csv-1.0", "rel/commons-csv-1.2", "rel/commons-csv-1.5", "rel/commons-csv-1.6",
        #   "rel/commons-csv-1.7"]),
        # (ProjectName.CommonsBeanUtils,
        #  ["BEANUTILS_1_9_3", "BEANUTILS_1_8_0_BETA", "BEANUTILS_1_8_3", "BEANUTILS_1_8_2", "BEANUTILS_1_8_0"]),
        # (ProjectName.CommonsNet, ["NET_3_3", "NET_2_2", "NET_2_0_RC_3", "NET_3_1", "NET_3_0_1"]),
        # (ProjectName.Continuum,
        #  ["continuum-1.3.2", "continuum-parent-1.1-beta-3", "continuum-1.4.0", "continuum-1.3.1", "continuum-1.3.8"])
        # (ProjectName.ServiceComb, ["0.1.0-m2"]),
        # (ProjectName.CommonsCompress, ["rel/1.3", "rel/1.4.1", "rel/1.5", "rel/1.19"]),
        # (ProjectName.Drill, ["drill-0.1.0", "0.6.0-incubating", "drill-0.9.0", "drill-1.1.0", "drill-1.11.0"])
        # (ProjectName.Tapestry5, ["5.0.4", "5.0.5", "5.0.6", "5.0.10", "5.1-dev-branch-base"])


    ]
    with Pool() as p:
        ris = p.map(execute, enumerate(projects))
        print(ris)
