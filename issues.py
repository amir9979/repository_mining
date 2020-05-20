import jira
from caching import cached
import json


class Issue(object):
    def __init__(self, issue):
        self.key = issue.key.strip()
        self.type = issue.fields.issuetype.name.lower()
        # self.issue_url = issue

@cached("apache_jira")
def get_jira_issues(project_name, url, bunch=100):
    jira_conn = jira.JIRA(url)
    all_issues=[]
    extracted_issues = 0
    while True:
        issues = jira_conn.search_issues("project={0}".format(project_name), maxResults=bunch, startAt=extracted_issues)
        all_issues.extend(issues)
        extracted_issues=extracted_issues+bunch
        if len(issues) < bunch:
            break
    return list(map(lambda issue: Issue(issue), all_issues))

if __name__ == "__main__":
    to_cache = [u'DL',u'MINDEXER',u'RAMPART',u'SAMZA',u'TRINIDAD',u'FUNCTOR',u'AURORA',u'VELTOOLS',u'FILEUPLOAD',u'CRUNCH',u'JACOB',u'JOHNZON',u'MARMOTTA',u'QPID',u'MNEMONIC',u'TRANSPORTS',u'MEECROWAVE',u'JDKIM',u'WINK',u'MPATCH',u'DBCP',u'CRYPTO',u'JEXL',u'CURATOR',u'WAGON',u'MJLINK',u'CALCITE',u'WEAVER',u'QPIDJMS',u'DIRECTMEMORY',u'NIFI',u'EMAIL',u'NUTCH',u'OPENWIRE',u'MJAVADOC',u'DIRMINA',u'RAT',u'JUNEAU',u'MRESOLVER',u'OAK',u'STRATOS',u'VALIDATOR',u'JSPF',u'TILES',u'MDEP',u'ZOOKEEPER',u'AIRAVATA',u'MRAR',u'ROCKETMQ',u'OPENEJB',u'POSTAGE',u'MRRESOURCES',u'HARMONY',u'HADOOP',u'OPENJPA',u'SYNCOPE',u'SM',u'FOP',u'MACR',u'WSS',u'JENA',u'LOGGING',u'MPDF',u'ARCHETYPE',u'PROXY',u'HAMA',u'MRM',u'POOL',u'CLK',u'FTPSERVER',u'CLOUDSTACK',u'FREEMARKER',u'OFBIZ',u'FINERACT',u'MVERIFIER',u'METRON',u'WICKET',u'KAND',u'ARIES',u'ACCUMULO',u'MSHADE',u'APLO',u'MGPG',u'MTOOLCHAINS',u'KAFKA',u'FLINK',u'LANG',u'MAHOUT',u'METAMODEL',u'EAGLE',u'MPH',u'TIKA',u'AMBARI',u'VXQUERY',u'NIFIREG',u'CASSANDRA',u'MJDEPS',u'BATIK',u'RNG',u'REEF',u'HELIX',u'TINKERPOP',u'SYNAPSE',u'HCATALOG',u'ASTERIXDB',u'SHINDIG',u'IMAGING',u'MPLUGINTESTING',u'XERCESJ',u'TAP5',u'TOMEE',u'MREPOSITORY',u'AMQCLI',u'GERONIMO',u'MLINKCHECK',u'JUDDI',u'MPIR',u'ODFTOOLKIT',u'MCHANGELOG',u'BVAL',u'CAY',u'CHAINSAW',u'FEDIZ',u'BEANUTILS',u'OGNL',u'TAJO',u'CXF',u'OWB',u'JSIEVE',u'PHOENIX',u'ACE',u'PIVOT',u'MRESOURCES',u'GORA',u'IO',u'AMQ',u'MJAR',u'SQOOP',u'OLTU',u'CONNECTORS',u'GEODE',u'CHUKWA',u'OODT',u'KALUMET',u'TEZ',u'MEJB',u'DELTASPIKE',u'JELLY',u'SB',u'JCLOUDS',u'RANGER',u'MEAR',u'ARTEMIS',u'SENTRY',u'CODEC',u'DDLUTILS',u'TEXT',u'SAND',u'GIRAPH',u'BIGTOP',u'CONFIGURATION',u'MIME4J',u'MSITE',u'OPENNLP',u'STORM',u'DATAFU',u'MDOAP',u'MCHANGES',u'DOXIA',u'ZEPPELIN',u'SUREFIRE',u'MYFACESTEST',u'TWILL',u'CONTINUUM',u'MCLEAN',u'RIVER',u'KYLIN',u'DOXIATOOLS',u'JSEC',u'MDEPLOY',u'AUTOTAG',u'SSHD',u'RAVE',u'MCOMPILER',u'MINSTALL',u'SANSELAN',u'AVRO',u'COMPRESS',u'HADOOP',u'SHIRO',u'EMPIREDB',u'BSF',u'CMIS',u'DIGESTER',u'XMLBEANS',u'DIRSTUDIO',u'FALCON',u'NET',u'TOBAGO',u'MASSEMBLY',u'SAVAN',u'MINVOKER',u'ETCH',u'PDFBOX',u'JXR',u'GROOVY',u'MCHECKSTYLE',u'MWAR',u'MJMOD',u'DBUTILS',u'LENS',u'ABDERA',u'MSTAGE',u'MSOURCES',u'ATLAS',u'HIVE',u'MRUNIT',u'MPLUGIN',u'ODE',u'CXFXJC',u'NUMBERS',u'BOOKKEEPER',u'DERBY',u'OPENMEETINGS',u'MPMD',u'KARAF',u'DOXIASITETOOLS',u'DRILL',u'SIS',u'TREQ',u'CHAIN',u'SYSTEMML',u'IGNITE',u'CSV',u'HBASE',u'STANBOL',u'MANTRUN',u'USERGRID',u'JXPATH',u'COCOON',u'WOOKIE',u'SCM',u'JCI',u'JCS',u'FLUME',u'NUVEM',u'OOZIE',u'JCRVLT',u'CTAKES',u'BEAM',u'CLEREZZA',u'STREAMS',u'CLI',u'MJDEPRSCAN',u'FELIX',u'MATH',u'WHIRR',u'MYFACES',u'JSPWIKI',u'SMXCOMP',u'VYSPER',u'CAMEL',u'HUPA',u'VFS',u'HDFS',u'MSCMPUB',u'GERONIMODEVTOOLS',u'KNOX',u'MANT',u'MNG',u'ISIS',u'SCXML',u'COLLECTIONS',u'OCM',u'EXEC',u'PIG',u'BCEL']
    for project_name in to_cache:
        try:
            issues = get_jira_issues(project_name, r"http://issues.apache.org/jira")
            with open(r"C:\temp\issues\{0}.json".format(project_name), "wb") as f:
                f.write(json.dumps(map(lambda i: i.issue.raw, issues)))
        except:
            pass