import os
from enum import Enum

from config import Config


class Project2():
    def __init__(self, github_name, description, github_user, jira_names, bz_names, jira_url, bz_url):
        self.github_name = github_name
        self.github_user = github_user
        self.jira_names = jira_names
        self.bz_names = bz_names
        self.description = description
        self.jira_url = jira_url
        self.bz_url = bz_url
        self.path = os.path.join(Config().config['REPO']['RepoDir'], self.github_name)


class Project():
    def __init__(self, github_name, jira_name, description=''):
        self.github_name = github_name
        self.jira_name = jira_name
        self.description = description
        self.path = os.path.join(Config().config['REPO']['RepoDir'], self.github_name)


class ProjectName(Enum):
    Camel = Project("camel", "CAMEL")
    Hadoop = Project("hadoop", "HADOOP")
    Flink = Project("flink", "FLINK")
    Kafka = Project("kafka", "KAFKA")
    OpenMeetings = Project("openmeetings", "OPENMEETINGS")
    Karaf = Project("karaf", "KARAF")
    Hbase = Project("hbase", "HBASE")
    Netbeans = Project("netbeans", "NETBEANS")
    UimaRuta = Project("uima-ruta", "UIMA")
    Lucene = Project("lucene-solr", "LUCENE")
    DeltaSpike = Project("deltaspike", "DELTASPIKE")
    JackrabbitOak = Project("jackrabbit-oak", "OAK")
    Pulsar = Project("pulsar", "PULSAR")
    Ofbiz = Project("ofbiz", "OFBIZ")
    Cayenne = Project("cayenne", "CAY")
    CommonsCodec = Project("commons-codec", "CODEC")
    Parquet = Project("parquet-mr", "PARQUET")
    Kylin = Project("kylin", "KYLIN")
    Hive = Project("hive", "HIVE")
    CommonsValidator = Project("commons-validator", "VALIDATOR")
    commonsvalidator = Project2('commons-validator', 'apache', 'Apache Commons Validator',
                                  ['VALIDATOR', 'VALIDATOR'], [], 'http://issues.apache.org/jira',
                                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    Surefire = Project("maven-surefire", "SUREFIRE")
    Syncope = Project("syncope", "SYNCOPE")
    CommonsMath = Project("commons-math", "MATH")
    Tomcat = Project("tomcat", "MTOMCAT")
    Atlas = Project("atlas", "ATLAS")
    Struts = Project("struts", "STR")
    Tika = Project("tika", "TIKA")
    ServiceComb = Project("servicecomb-java-chassis", "SCB")
    Ranger = Project("ranger", "RANGER")
    Cassandra = Project("cassandra", "CASSANDRA")
    CXF = Project("cxf", "CXF")
    Avro = Project("avro", "AVRO")
    Nifi = Project("nifi", "NIFI")
    Bookkeeper = Project("bookkeeper", "BOOKKEEPER")
    Clerezza = Project("clerezza", "CLEREZZA")
    SystemML = Project("systemml", "SYSTEMML")
    AsterixDB = Project("asterixdb", "ASTERIXDB")
    Unomi = Project("unomi", "UNOMI")
    Maven = Project("maven", "MNG")
    Zeppelin = Project("zeppelin", "ZEPPELIN")
    CommonsCollections = Project("commons-collections", "COLLECTIONS")
    Jena = Project("jena", "JENA")
    Calcite = Project("calcite", "CALCITE")
    Tez = Project("tez", "TEZ")
    CommonsLang = Project("commons-lang", "LANG")
    ActiveMQ = Project("activemq", "AMQ")
    Curator = Project("curator", "CURATOR")
    Phoenix = Project("phoenix", "PHOENIX")
    Samza = Project("samza", "SAMZA")
    Nutch = Project("nutch", "NUTCH")
    QpidJMS = Project("qpid-jms", "QPIDJMS")
    DirectoryKerby = Project("directory-kerby", "DIRKRB")
    Juneau = Project("juneau", "JUNEAU")
    MyFacesTobago = Project("myfaces-tobago", "TOBAGO")
    Isis = Project("isis", "ISIS")
    Wicket = Project("wicket", "WICKET")
    Santuario = Project("santuario-java", "SANTUARIO")
    Helix = Project("helix", "HELIX")
    Storm = Project("storm", "STORM")
    Airavata = Project("airavata", "AIRAVATA")
    MyFaces = Project("myfaces", "MYFACES")
    CommonsDBCP = Project("commons-dbcp", "DBCP")
    CommonsVFS = Project("commons-vfs", "VFS")
    OpenNLP = Project("opennlp", "OPENNLP")
    Tomee = Project("tomee", "TOMEE")
    TinkerPop = Project("tinkerpop", "TINKERPOP")
    DirectoryServer = Project("directory-server", "DIRSERVER")
    CommonsCompress = Project("commons-compress", "COMPRESS")
    Accumulo = Project("accumulo", "ACCUMULO")
    Giraph = Project("giraph", "GIRAPH")
    Johnzon = Project("johnzon", "JOHNZON")
    JClouds = Project("jclouds", "JCLOUDS")
    ManifoldCF = Project("manifoldcf", "CONNECTORS")
    Shiro = Project("shiro", "SHIRO")
    Knox = Project("knox", "KNOX")
    Drill = Project("drill", "DRILL")
    Crunch = Project("crunch", "CRUNCH")
    CommonsIO = Project("commons-io", "IO")
    CommonsCLI = Project("commons-cli", "CLI")
    Jackrabbit = Project("jackrabbit", "JCR")
    OpenWebBeans = Project("openwebbeans", "OWB")
    FOP = Project("xmlgraphics-fop", "FOP")
    Tajo = Project("tajo", "TAJO")
    CommonsEmail = Project("commons-email", "EMAIL")
    DirectoryStudio = Project("directory-studio", "DIRSTUDIO")
    Tapestry5 = Project("tapestry-5", "TAP5")
    Archiva = Project("archiva", "MRM")
    Olingo = Project("olingo-odata4", "OLINGO")
    OpenJPA = Project("openjpa", "OPENJPA")
    CommonsJexl = Project("commons-jexl", "JEXL")
    Roller = Project("roller", "ROL")
    Reef = Project("reef", "REEF")

    ActiveMQArtemis = Project("activemq-artemis", "ARTEMIS")
    Beam = Project("beam", "BEAM")
    Metron = Project("metron", "METRON")
    Plc4x = Project("plc4x", "PLC4X")

    Cocoon = Project("cocoon", "COCOON")
    CarbonData = Project("carbondata", "CARBONDATA")
    CommonsCSV = Project("commons-csv", "CSV")

    CommonsBeanUtils = Project("commons-beanutils", "BEANUTILS")
    CommonsNet = Project("commons-net", "NET")
    Continuum = Project("continuum", "CONTINUUM")


    # Projects that failed selection
    # Groovy = Project("groovy", "GROOVY")
    # Ignite = Project("ignite", "IGNITE")
    # Bahir = Project("bahir", "BAHIR")
    # CommonsDigester = Project("commons-digester", "DIGESTER")
    # CommonsDaemon = Project("commons-daemon", "DAEMON")
    # Buildr = Project("buildr", "BUILDR")
    # Click = Project("click", "CLK")
    # Aries = Project("aries", "ARIES")
    # Bigtop = Project("bigtop", "BIGTOP")
    # VXQuery = Project("vxquery", "VXQUERY")
    # Brooklyn = Project("incubator-brooklyn", "BROOKLYN")
    # CloudStack = Project("cloudstack", "CLOUDSTACK")
    # CommonsCrypto = Project("commons-crypto", "CRYPTO")
    # GeodeBenchmarks = Project("geode-benchmarks", "GEODE")
    # Mina = Project("mina", "DIRMINA")
    # Submarine = Project("submarine", "SUBMARINE")
    # Griffin = Project("griffin", "GRIFFIN")
    # CommonsImaging = Project("commons-imaging", "IMAGING")
    # RocketMQ = Project("rocketmq", "ROCKETMQ")
    # Synapse = Project("synapse", "SYNAPSE")
    # Fineract = Project("fineract", "FINERACT")
    # Dubbo = Project("dubbo", "DUBBO")

    # def github(self):
    #     return self.github()
    #
    # def jira(self):
    #     return self.jira()
    #
    # def path(self):
    #     return self.path()

if __name__ == "__main__":
    ans = []
    for i in range(8):
        ans.extend(list(map(lambda x: 'gh issue create -t {0} -b "--select_verions {1}"'.format(x.name, i), ProjectName)))
    print("\n".join(ans))