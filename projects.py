import os
from enum import Enum

from config import Config


class Project():
    def __init__(self, github_name, github_user, description, jira_names, bz_names, jira_url, bz_url):
        self.github_name = github_name
        self.github_user = github_user
        self.jira_names = jira_names
        self.bz_names = bz_names
        self.description = description
        self.jira_url = jira_url
        self.bz_url = bz_url
        self.path = os.path.join(Config().config['REPO']['RepoDir'], self.github_name)


class ProjectDeprecated():
    def __init__(self, github_name, jira_name, description=''):
        self.github_name = github_name
        self.jira_name = jira_name
        self.description = description
        self.path = os.path.join(Config().config['REPO']['RepoDir'], self.github_name)


class ProjectName(Enum):
    kafka = Project('kafka', 'apache', 'Mirror of Apache Kafka', ['KAFKA'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    flink = Project('flink', 'apache', 'Apache Flink', ['FLINK'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    hadoop = Project('hadoop', 'apache', 'Apache Hadoop', ['HADOOP'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    zookeeper = Project('zookeeper', 'apache', 'Apache ZooKeeper', ['ZOOKEEPER'], [], 'http://issues.apache.org/jira',
                        'bz.apache.org/bugzilla/xmlrpc.cgi')
    cassandra = Project('cassandra', 'apache', 'Mirror of Apache Cassandra', ['CASSANDRA'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    storm = Project('storm', 'apache', 'Mirror of Apache Storm', ['STORM'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    tomcat = Project('tomcat', 'apache', 'Apache Tomcat', [],
                     ['Tomcat 3', 'Tomcat Modules', 'Tomcat 4', 'Tomcat 10', 'Tomcat 5', 'Tomcat 8', 'Tomcat 6',
                      'Tomcat 9', 'Tomcat Native', 'Tomcat 7', 'Tomcat Connectors'], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    zeppelin = Project('zeppelin', 'apache',
                       'Web-based notebook that enables data-driven, interactive data analytics and collaborative documents with SQL, Scala and more.',
                       ['ZEPPELIN'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jmeter = Project('jmeter', 'apache', 'Apache JMeter', [], ['JMeter'], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    beam = Project('beam', 'apache', 'Apache Beam is a unified programming model for Batch and Streaming', ['BEAM'], [],
                   'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    lucenesolr = Project('lucene-solr', 'apache', 'Apache Lucene and Solr open-source search software', ['SOLR'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    groovy = Project('groovy', 'apache',
                     'Apache Groovy: A powerful multi-faceted programming language for the JVM platform', ['GROOVY'],
                     [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ignite = Project('ignite', 'apache', 'Apache Ignite', ['IGNITE'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    camel = Project('camel', 'apache',
                    'Apache Camel is an open source integration framework that empowers you to quickly and easily integrate various systems consuming or producing data.',
                    ['CAMEL'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    hive = Project('hive', 'apache', 'Apache Hive', ['HIVE'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    shiro = Project('shiro', 'apache', 'Apache Shiro', ['SHIRO'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    kylin = Project('kylin', 'apache', 'Apache Kylin', ['KYLIN'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    curator = Project('curator', 'apache', 'Apache Curator', ['CURATOR'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    nifi = Project('nifi', 'apache', 'Apache NiFi', ['NIFI'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    maven = Project('maven', 'apache', 'Apache Maven core', ['MNG'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    calcite = Project('calcite', 'apache', 'Apache Calcite', ['CALCITE'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    nutch = Project('nutch', 'apache', 'Apache Nutch is an extensible and scalable web crawler', ['NUTCH'], [],
                    'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonslang = Project('commons-lang', 'apache', 'Mirror of Apache Commons Lang', ['LANG'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    flume = Project('flume', 'apache', 'Mirror of Apache Flume', ['FLUME'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    mahout = Project('mahout', 'apache', 'Mirror of Apache Mahout', ['MAHOUT'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    geode = Project('geode', 'apache', 'Apache Geode', ['GEODE'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    activemq = Project('activemq', 'apache', 'Mirror of Apache ActiveMQ', ['AMQ'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    avro = Project('avro', 'apache', 'Apache Avro is a data serialization system.', ['AVRO'], [],
                   'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    hudi = Project('hudi', 'apache', 'Upserts, Deletes And Incremental Processing on Big Data.', ['HUDI'], [],
                   'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    drill = Project('drill', 'apache', 'Apache Drill', ['DRILL'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    ambari = Project('ambari', 'apache', 'Mirror of Apache Ambari', ['AMBARI'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    pdfbox = Project('pdfbox', 'apache', 'Mirror of Apache PDFBox', ['PDFBOX'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    tinkerpop = Project('tinkerpop', 'apache', 'Apache TinkerPop - a graph computing framework', ['TINKERPOP'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tika = Project('tika', 'apache', 'Mirror of Apache Tika', ['TIKA'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    bookkeeper = Project('bookkeeper', 'apache', 'Apache Bookkeeper', ['BOOKKEEPER'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    poi = Project('poi', 'apache', 'Mirror of Apache POI', [], ['POI'], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    logginglog4j2 = Project('logging-log4j2', 'apache',
                            'Apache Log4j 2 is an upgrade to Log4j that provides significant improvements over its predecessor, Log4j 1.x, and provides many of the improvements available in Logback while fixing some inherent problems in Logbacks architecture.',
                            ['LOG4J2'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    iotdb = Project('iotdb', 'apache', 'Apache IoTDB', ['IOTDB'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    opennlp = Project('opennlp', 'apache', 'Mirror of Apache OpenNLP', ['OPENNLP'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    phoenix = Project('phoenix', 'apache', 'Mirror of Apache Phoenix', ['PHOENIX', 'PNIX'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    accumulo = Project('accumulo', 'apache', 'Apache Accumulo', ['ACCUMULO'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    systemds = Project('systemds', 'apache', 'Mirror of Apache SystemML', ['SYSTEMDS'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    metron = Project('metron', 'apache', 'Apache Metron', ['METRON'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsio = Project('commons-io', 'apache', 'Mirror of Apache Commons IO', ['IO'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atlas = Project('atlas', 'apache', 'Apache Atlas', ['ATLAS'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    log4j = Project('log4j', 'apache', 'Mirror of Apache log4j', [], ['Log4j - Now in Jira'],
                    'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ofbiz = Project('ofbiz', 'apache', 'Apache OFBiz - Main development has moved to the ofbiz-frameworks repository.',
                    ['OFBIZ'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jena = Project('jena', 'apache', 'Mirror of Apache Jena', ['JENA'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    cxf = Project('cxf', 'apache', 'Apache CXF', ['CXF'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    samza = Project('samza', 'apache', 'Mirror of Apache Samza', ['SAMZA'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    activemqartemis = Project('activemq-artemis', 'apache', 'Mirror of Apache ActiveMQ Artemis', ['ARTEMIS'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    pig = Project('pig', 'apache', 'Mirror of Apache Pig', ['PIG'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    oozie = Project('oozie', 'apache', 'Mirror of Apache Oozie', ['OOZIE'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    isis = Project('isis', 'apache',
                   'Apache Isis™ software is a framework for rapidly developing domain-driven apps in Java. Write your business logic in entities, domain services or view models, and the framework dynamically generates a representation of that domain model as a webapp or as a RESTful API. For prototyping or production. ',
                   ['ISIS'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    wicket = Project('wicket', 'apache', 'Apache Wicket - Component-based Java web framework', ['WICKET'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    karaf = Project('karaf', 'apache', 'Mirror of Apache Karaf', ['KARAF'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscollections = Project('commons-collections', 'apache', 'Mirror of Apache Commons Collections',
                                 ['COLLECTIONS'], [], 'http://issues.apache.org/jira',
                                 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ranger = Project('ranger', 'apache', 'Mirror of Apache Ranger', ['RANGER'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    openmeetings = Project('openmeetings', 'apache', 'Mirror of Apache Openmeetings', ['OPENMEETINGS'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsmath = Project('commons-math', 'apache', 'Apache Commons Math', ['MATH'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    wswss4j = Project('ws-wss4j', 'apache', 'Apache WebServices - WSS4J', ['WSS'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    continuum = Project('continuum', 'apache', 'Mirror of Apache Continuum', ['CONTINUUM'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenremoteresourcesplugin = Project('maven-remote-resources-plugin', 'apache',
                                         'Apache Maven Remote Resources Plugin', ['MRRESOURCES'], [],
                                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenearplugin = Project('maven-ear-plugin', 'apache', 'Apache Maven EAR Plugin', ['MEAR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenpatchplugin = Project('maven-patch-plugin', 'apache', 'Apache Maven Patch Plugin', ['MPATCH'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorambari = Project('incubator-ambari', 'apache', 'Mirror of Apache Ambari (Incubating)', ['AMBARI'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjxr = Project('maven-jxr', 'apache', 'Apache Maven JXR (Plugin)', ['JXR'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimodevtools = Project('geronimo-devtools', 'apache', 'Mirror of Apache Geronimo Devtools',
                               ['GERONIMODEVTOOLS'], [], 'http://issues.apache.org/jira',
                               'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenchangesplugin = Project('maven-changes-plugin', 'apache', 'Apache Maven Changes Plugin', ['MCHANGES'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendoxiasitetools = Project('maven-doxia-sitetools', 'apache', 'Apache Maven Doxia Sitetools', ['DOXIASITETOOLS'],
                                  [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenrarplugin = Project('maven-rar-plugin', 'apache', 'Apache Maven RAR Plugin', ['MRAR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfacestrinidad = Project('myfaces-trinidad', 'apache', 'Apache MyFaces Trinidad', ['TRINIDAD'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    creadurwhisker = Project('creadur-whisker', 'apache', 'Mirror of Apache Whisker', ['WHISKER'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    archivasandbox = Project('archiva-sandbox', 'apache', 'Apache Archiva sandbox',
                             ['SB', 'SANDBOX', 'VELOCITYSB', 'TILESSB'], [], 'http://issues.apache.org/jira',
                             'bz.apache.org/bugzilla/xmlrpc.cgi')
    wsxmlschema = Project('ws-xmlschema', 'apache', 'Apache Web Services - XmlSchema', ['XMLSCHEMA'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    accumuloproxy = Project('accumulo-proxy', 'apache', 'Apache Accumulo Proxy', ['PROXY'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    minaasyncweb = Project('mina-asyncweb', 'apache', 'Apache Mina Async Web', ['ASYNCWEB'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticonami = Project('attic-onami', 'apache', 'Apache Onami (retired)', ['ONAMI'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimoyoko = Project('geronimo-yoko', 'apache', 'Mirror of Apache Geronimo yoko', ['YOKO'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendoapplugin = Project('maven-doap-plugin', 'apache', 'Apache Maven DOAP Plugin', ['MDOAP'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjdeprscanplugin = Project('maven-jdeprscan-plugin', 'apache', 'Apache Maven JDeprscan Plugin', ['MJDEPRSCAN'],
                                   [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatortwill = Project('incubator-twill', 'apache', 'Mirror of Apache Twill', ['TWILL'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamespostage = Project('james-postage', 'apache', 'Mirror of Apache James postage', ['POSTAGE'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    rampart = Project('rampart', 'apache', 'Mirror of Apache Rampart', ['RAMPART'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenacrplugin = Project('maven-acr-plugin', 'apache', 'Apache Maven ACR Plugin', ['MACR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenlinkcheckplugin = Project('maven-linkcheck-plugin', 'apache', 'Apache Maven Linkcheck Plugin', ['MLINKCHECK'],
                                   [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tomee = Project('tomee', 'apache', 'Apache TomEE', ['TOMEE'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonspool = Project('commons-pool', 'apache', 'Mirror of Apache Commons Pool', ['POOL'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    minasshd = Project('mina-sshd', 'apache', 'Mirror of Apache MINA SSHD', ['SSHD'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticapexcore = Project('attic-apex-core', 'apache', 'Mirror of Apache Apex core', ['APEXCORE'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jackrabbitoak = Project('jackrabbit-oak', 'apache', 'Mirror of Apache Jackrabbit Oak', ['OAK'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavensurefire = Project('maven-surefire', 'apache', 'Apache Maven Surefire', ['SUREFIRE'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    helix = Project('helix', 'apache', 'Mirror of Apache Helix', ['HELIX'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscodec = Project('commons-codec', 'apache', 'Apache Commons Codec', ['CODEC'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ant = Project('ant', 'apache', 'Apache Ant is a Java-based build tool.', [], ['Ant'],
                  'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    archiva = Project('archiva', 'apache', 'Apache Archiva', ['MRM'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsdbutils = Project('commons-dbutils', 'apache', 'Mirror of Apache Commons DbUtils', ['DBUTILS'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsdbcp = Project('commons-dbcp', 'apache', 'Mirror of Apache Commons DBCP', ['DBCP'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    cayenne = Project('cayenne', 'apache', 'Mirror of Apache Cayenne', ['CAY'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscsv = Project('commons-csv', 'apache', 'Mirror of Apache Commons CSV', ['CSV'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    httpcomponentscore = Project('httpcomponents-core', 'apache', 'Mirror of Apache HttpCore', ['MYFACES'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    cxffediz = Project('cxf-fediz', 'apache', 'Mirror of Apache CXF', ['FEDIZ'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavensiteplugin = Project('maven-site-plugin', 'apache', 'Apache Maven Site Plugin', ['MSITE'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    minaftpserver = Project('mina-ftpserver', 'apache', 'Apache Mina FTP Server', ['FTPSERVER'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticrave = Project('attic-rave', 'apache', 'Mirror of Apache Rave', ['RAVE'], [], 'http://issues.apache.org/jira',
                        'bz.apache.org/bugzilla/xmlrpc.cgi')
    juddi = Project('juddi', 'apache', 'Mirror of Apache jUDDI', ['JUDDI'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfacestobago = Project('myfaces-tobago', 'apache', 'Apache MyFaces Tobago', ['TOBAGO'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenprojectinforeportsplugin = Project('maven-project-info-reports-plugin', 'apache',
                                            'Apache Maven Project Info Reports Plugin', ['MPIR'], [],
                                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    cxfxjcutils = Project('cxf-xjc-utils', 'apache', 'Mirror of Apache CXF', ['CXFXJC'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    maveninvokerplugin = Project('maven-invoker-plugin', 'apache', 'Apache Maven Invoker Plugin', ['MINVOKER'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimoxbean = Project('geronimo-xbean', 'apache', 'Mirror of Apache Geronimo xbean', ['XBEAN'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavensourceplugin = Project('maven-source-plugin', 'apache', 'Apache Maven Source Plugin', ['MSOURCES'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscli = Project('commons-cli', 'apache', 'Mirror of Apache Commons CLI', ['CLI'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsbeanutils = Project('commons-beanutils', 'apache', 'Apache Commons Beanutils', ['BEANUTILS'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonstext = Project('commons-text', 'apache', 'Mirror of Apache Commons Text', ['TEXT'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    asterixdb = Project('asterixdb', 'apache', 'Mirror of Apache AsterixDB', ['ASTERIXDB'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscompress = Project('commons-compress', 'apache', 'Mirror of Apache Commons Compress', ['COMPRESS'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticstratos = Project('attic-stratos', 'apache', 'Mirror of Apache Stratos', ['STRATOS'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    metamodel = Project('metamodel', 'apache', 'Mirror of Apache Metamodel', ['METAMODEL'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsbcel = Project('commons-bcel', 'apache', 'Apache Commons BCEL', ['BCEL'], ['BCEL - Now in Jira'],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsnet = Project('commons-net', 'apache', 'Apache Commons Net', ['NET'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsvfs = Project('commons-vfs', 'apache', 'Apache Commons VFS', ['VFS'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticapexmalhar = Project('attic-apex-malhar', 'apache', 'Mirror of Apache Apex malhar', ['APEXMALHAR'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    deltaspike = Project('deltaspike', 'apache', 'Mirror of Apache Deltaspike', ['DELTASPIKE'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    hama = Project('hama', 'apache', 'Mirror of Apache Hama', ['HAMA'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    tajo = Project('tajo', 'apache', 'Mirror of Apache Tajo', ['TAJO'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    syncope = Project('syncope', 'apache', 'Apache Syncope', ['SYNCOPE'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    xmlgraphicsbatik = Project('xmlgraphics-batik', 'apache', 'Mirror of Apache Batik', ['BATIK'],
                               ['Batik - Now in Jira'], 'http://issues.apache.org/jira',
                               'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsvalidator = Project('commons-validator', 'apache', 'Apache Commons Validator', ['VALIDATOR'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    xmlgraphicsfop = Project('xmlgraphics-fop', 'apache', 'Mirror of Apache FOP', ['FOP'], ['Fop - Now in Jira'],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsconfiguration = Project('commons-configuration', 'apache', 'Apache Commons Configuration', ['CONFIGURATION'],
                                   [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    knox = Project('knox', 'apache', 'Mirror of Apache Knox', ['KNOX'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    qpid = Project('qpid', 'apache', 'Mirror of Apache Qpid', ['QPID'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    sentry = Project('sentry', 'apache', 'Mirror of Apache Sentry', ['SENTRY'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    crunch = Project('crunch', 'apache', 'Mirror of Apache Crunch (Incubating)', ['CRUNCH'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tiles = Project('tiles', 'apache', 'Mirror of Apache Tiles', ['TILES'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenarchetype = Project('maven-archetype', 'apache', 'Apache Maven Archetype (Plugin)', ['ARCHETYPE'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    gora = Project('gora', 'apache', 'Mirror of Apache Gora', ['GORA'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    falcon = Project('falcon', 'apache', 'Mirror of Apache Falcon', ['FALCON'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    roller = Project('roller', 'apache', 'Mirror of Apache Roller', ['ROL'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    jclouds = Project('jclouds', 'apache', 'Mirror of Apache jclouds', ['JCLOUDS'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    mnemonic = Project('mnemonic', 'apache', 'Apache Mnemonic - A non-volatile hybrid memory storage oriented library',
                       ['MNEMONIC'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    openjpa = Project('openjpa', 'apache', 'Apache OpenJPA', ['OPENJPA'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    joshua = Project('joshua', 'apache', 'Apache Joshua', ['JOSHUA'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    tapestry5 = Project('tapestry-5', 'apache', 'Mirror of Apache Tapestry 5', ['TAP5'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsjexl = Project('commons-jexl', 'apache', 'Apache Commons Jexl', ['JEXL'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsemail = Project('commons-email', 'apache', 'Apache Commons Email', ['EMAIL'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    httpasyncclient = Project('httpasyncclient', 'apache', 'Mirror of Apache HttpComponents HttpAsyncClient',
                              ['HTTPASYNC'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavencompilerplugin = Project('maven-compiler-plugin', 'apache', 'Apache Maven Compiler Plugin', ['MCOMPILER'], [],
                                  'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    airavata = Project('airavata', 'apache', 'A general purpose Distributed Systems Framework', ['AIRAVATA'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jspwiki = Project('jspwiki', 'apache',
                      'Apache JSPWiki is a leading open source WikiWiki engine, feature-rich and built around standard JEE components (Java, servlets, JSP)',
                      ['JSPWIKI'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenscm = Project('maven-scm', 'apache', 'Apache Maven SCM (Plugin)', ['SCM'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    streams = Project('streams', 'apache', 'Apache Streams', ['STREAMS'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    directorystudio = Project('directory-studio', 'apache', 'Apache Directory Studio', ['DIRSTUDIO', 'STUDIO'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    shindig = Project('shindig', 'apache', 'Mirror of Apache Shindig (incubating)', ['SHINDIG'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenshadeplugin = Project('maven-shade-plugin', 'apache', 'Apache Maven Shade Plugin', ['MSHADE'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ftpserver = Project('ftpserver', 'apache', 'Mirror of Apache FtpServer', ['FTPSERVER'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    twill = Project('twill', 'apache', 'Mirror of Apache Twill', ['TWILL'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendependencyplugin = Project('maven-dependency-plugin', 'apache', 'Apache Maven Dependency Plugin', ['MDEP'], [],
                                    'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    juneau = Project('juneau', 'apache', 'Apache Juneau is a single cohesive framework', ['JUNEAU'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfaces = Project('myfaces', 'apache', 'Apache MyFaces Core', ['MYFACES'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    lens = Project('lens', 'apache', 'Mirror of Apache Lens', ['LENS'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    hcatalog = Project('hcatalog', 'apache', 'Mirror of Apache HCatalog', ['HCATALOG'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    oodt = Project('oodt', 'apache', 'Mirror of Apache OODT', ['OODT'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    qpidjms = Project('qpid-jms', 'apache', 'Mirror of Apache Qpid JMS', ['QPIDJMS'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    openwebbeans = Project('openwebbeans', 'apache', 'Apache OpenWebBeans', ['OWB'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    openwebbeansmeecrowave = Project('openwebbeans-meecrowave', 'apache', 'Apache OpenWebBeans meecrowave',
                                     ['MEECROWAVE'], [], 'http://issues.apache.org/jira',
                                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenindexer = Project('maven-indexer', 'apache', 'Apache Maven Indexer', ['MINDEXER'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    antivy = Project('ant-ivy', 'apache', 'Mirror of Apache Ant Ivy', ['IVY'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticode = Project('attic-ode', 'apache', 'Mirror of Apache ODE', ['ODE'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenassemblyplugin = Project('maven-assembly-plugin', 'apache', 'Apache Maven Assembly Plugin', ['MASSEMBLY'], [],
                                  'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenwagon = Project('maven-wagon', 'apache', 'Apache Maven Wagon', ['WAGON'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    johnzon = Project('johnzon', 'apache', 'Mirror of Apache Johnzon', ['JOHNZON'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    xmlbeans = Project('xmlbeans', 'apache', 'Mirror of Apache XMLBeans', ['XMLBEANS'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    sanselan = Project('sanselan', 'apache', 'Mirror of Apache Sanselan (incubating)', ['SANSELAN'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamesmime4j = Project('james-mime4j', 'apache', 'Mirror of Apache James Mime4j', ['MIME4J'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjavadocplugin = Project('maven-javadoc-plugin', 'apache', 'Apache Maven Javadoc Plugin', ['MJAVADOC'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jackrabbitfilevault = Project('jackrabbit-filevault', 'apache', 'Apache Jackrabbit FileVault', ['JCRVLT'], [],
                                  'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavencheckstyleplugin = Project('maven-checkstyle-plugin', 'apache', 'Apache Maven Checkstyle Plugin',
                                    ['MCHECKSTYLE'], [], 'http://issues.apache.org/jira',
                                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    cxfdosgi = Project('cxf-dosgi', 'apache', 'Mirror of Apache CXF', ['DOSGI'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    phoenixtephra = Project('phoenix-tephra', 'apache', 'Mirror of Apache Tephra (Incubating)', ['TEPHRA'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenplugintools = Project('maven-plugin-tools', 'apache', 'Apache Maven Plugin Tools', ['MPLUGIN'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    empiredb = Project('empire-db', 'apache', 'Mirror of Apache Empire-db', ['EMPIREDB'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    xerces2j = Project('xerces2-j', 'apache', 'Mirror of Apache Xerces2 Java', ['XERCESJ'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendeployplugin = Project('maven-deploy-plugin', 'apache', 'Apache Maven Deploy Plugin', ['MDEPLOY'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    portalspluto = Project('portals-pluto', 'apache', 'Mirror of Apache Pluto', ['PLUTO'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendoxia = Project('maven-doxia', 'apache', 'Apache Maven Doxia base', ['DOXIA'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenpmdplugin = Project('maven-pmd-plugin', 'apache', 'Apache Maven PMD Plugin', ['MPMD'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenwarplugin = Project('maven-war-plugin', 'apache', 'Apache Maven WAR Plugin', ['MWAR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    # Eclipse issues
    deeplearning4j = Project('deeplearning4j', 'eclipse',
                             'Eclipse Deeplearning4j, ND4J, DataVec and more - deep learning & linear algebra for Java/Scala with GPUs + Spark',
                             [], ['DeepLearning4J'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    che = Project('che', 'eclipse', 'The Kubernetes-Native IDE for Developer Teams', [], ['Che'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    openj9 = Project('openj9', 'eclipse',
                     'Eclipse OpenJ9: A Java Virtual Machine for OpenJDK thats optimized for small footprint, fast start-up, and high throughput.   Builds on Eclipse OMR (https://github.com/eclipse/omr) and combines with the Extensions for OpenJDK for OpenJ9 repo.',
                     [], ['openj9'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    eclipsecollections = Project('eclipse-collections', 'eclipse',
                                 'Eclipse Collections is a collections framework for Java with optimized data structures and a rich, functional and fluent API.',
                                 [], ['Collections'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    jgit = Project('jgit', 'eclipse', 'JGit project repository (jgit)', [], ['JGit'], 'None',
                   'bugs.eclipse.org/bugs/xmlrpc.cgi')
    milo = Project('milo', 'eclipse', ' Eclipse Milo™ - an open source implementation of OPC UA (IEC 62541).', [],
                   ['Milo'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    californium = Project('californium', 'eclipse', 'CoAP/DTLS Java Implementation ', [], ['Californium'], 'None',
                          'bugs.eclipse.org/bugs/xmlrpc.cgi')
    buildship = Project('buildship', 'eclipse', 'The Eclipse Plug-ins for Gradle project.', [], ['Buildship'], 'None',
                        'bugs.eclipse.org/bugs/xmlrpc.cgi')
    microprofile = Project('microprofile', 'eclipse',
                           'Repository for important documentation - the index to the project / community', [],
                           ['Microprofile'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    ceylon = Project('ceylon', 'eclipse', 'The Ceylon compiler, language module, and command line tools', [],
                     ['Ceylon'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    kura = Project('kura', 'eclipse', 'Eclipse Kura™ project - http://eclipse.org/kura', [], ['Kura'], 'None',
                   'bugs.eclipse.org/bugs/xmlrpc.cgi')
    lsp4j = Project('lsp4j', 'eclipse',
                    'A Java implementation of the language server protocol intended to be consumed by tools and language servers implemented in Java.',
                    [], ['Lsp4j'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    hawkbit = Project('hawkbit', 'eclipse', 'Eclipse hawkBit™', [], ['Hawkbit'], 'None',
                      'bugs.eclipse.org/bugs/xmlrpc.cgi')
    ditto = Project('ditto', 'eclipse', 'Eclipse Ditto Project', [], ['Ditto'], 'None',
                    'bugs.eclipse.org/bugs/xmlrpc.cgi')
    birt = Project('birt', 'eclipse', 'Eclipse BIRT™ The open source reporting and data visualization project. ', [],
                   ['BIRT'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    vorto = Project('vorto', 'eclipse', 'Vorto Project', [], ['Vorto'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    kapua = Project('kapua', 'eclipse', '', [], ['Kapua'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    jnosql = Project('jnosql', 'eclipse',
                     'Eclipse JNoSQL is a framework which has the goal to help Java developers to create Jakarta EE applications with NoSQL.',
                     [], ['JNoSQL'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    egit = Project('egit', 'eclipse', 'Eclipse Git Team Provider (EGit) project repository (egit)', [], ['EGit'],
                   'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    elk = Project('elk', 'eclipse', 'Eclipse Layout Kernel - Automatic layout for Java applications.', [], ['Elk'],
                  'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    gef = Project('gef', 'eclipse', 'Eclipse GEF™', [], ['GEF'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    xtextxtend = Project('xtext-xtend', 'eclipse', 'xtext-xtend', [], ['Xtend'], 'None',
                         'bugs.eclipse.org/bugs/xmlrpc.cgi')
    tycho = Project('tycho', 'eclipse', 'Tycho project repository (tycho)', [], ['Tycho'], 'None',
                    'bugs.eclipse.org/bugs/xmlrpc.cgi')
    sw360 = Project('sw360', 'eclipse', 'SW360 project', [], ['SW360'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    texlipse = Project('texlipse', 'eclipse', 'Eclipse Texlipse', [], ['Texlipse'], 'None',
                       'bugs.eclipse.org/bugs/xmlrpc.cgi')
    tahu = Project('tahu', 'eclipse',
                   'Eclipse Tahu addresses the existence of legacy SCADA/DCS/ICS protocols and infrastructures and provides a much-needed definition of how best to apply MQTT into these existing industrial operational environments.',
                   [], ['Tahu'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    jifa = Project('jifa', 'eclipse', '', [], ['Jifa'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    emf = Project('emf', 'eclipse', 'EMF project repository (emf)', [], ['EMF', 'EMF Services'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    eclemma = Project('eclemma', 'eclipse', ':waning_crescent_moon:　Java Code Coverage for Eclipse', [], ['Eclemma'],
                      'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    nebula = Project('nebula', 'eclipse', 'Nebula Project', [], ['Nebula'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    rap = Project('rap', 'eclipse', 'Rich Ajax Platform project repository (rap)', [], ['RAP'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    acceleo = Project('acceleo', 'eclipse', 'Acceleo project repository (acceleo)', [], ['Acceleo'], 'None',
                      'bugs.eclipse.org/bugs/xmlrpc.cgi')
    capella = Project('capella', 'eclipse', 'Open Source Solution for Model-Based Systems Engineering', [], ['Capella'],
                      'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    reddeer = Project('reddeer', 'eclipse', 'RedDeer Project', [], ['Reddeer'], 'None',
                      'bugs.eclipse.org/bugs/xmlrpc.cgi')
    ice = Project('ice', 'eclipse', 'Ice Project Main repo', [], ['Ice'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    Xpect = Project('Xpect', 'eclipse',
                    'This repository has been rewritten to move to the Eclipse Foundation. Find the old history here: https://github.com/TypeFox/Xpect',
                    [], ['xpect'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    swtbot = Project('swtbot', 'eclipse', 'SWTBot project repository (swtbot)', [], ['SWTBot'], 'None',
                     'bugs.eclipse.org/bugs/xmlrpc.cgi')
    swtchart = Project('swtchart', 'eclipse', '', [], ['SwtChart'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    xsemantics = Project('xsemantics', 'eclipse',
                         'Xsemantics is a DSL (implemented in Xtext itself) for writing type systems, reduction rules, interpreters (and in general relation rules) for languages implemented in Xtext. It then generates Java code that can be used in your language implemented in Xtext for scoping and validation (it can also generate a validator in Java).',
                         [], ['xsemantics'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    antenna = Project('antenna', 'eclipse', 'SW360 Antenna project', [], ['Antenna'], 'None',
                      'bugs.eclipse.org/bugs/xmlrpc.cgi')
    thym = Project('thym', 'eclipse', 'Thym Project', [], ['Thym'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    xtend = Project('xtend', 'eclipse', 'Xtend project repository (xtend)', [], ['Xtend'], 'None',
                    'bugs.eclipse.org/bugs/xmlrpc.cgi')
    keti = Project('keti', 'eclipse', '', [], ['Keti'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    gmftooling = Project('gmf-tooling', 'eclipse',
                         'Graphical Modeling Framework (GMF) Tooling project repository (gmf-tooling)', [],
                         ['GMF-Tooling'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    ecf = Project('ecf', 'eclipse', 'Eclipse Communication Framework (ECF) project repository (ecf)', [], ['ECF'],
                  'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    keyplejava = Project('keyple-java', 'eclipse', 'Keyple Java source', [], ['Java Server Faces'], 'None',
                         'bugs.eclipse.org/bugs/xmlrpc.cgi')
    triquetrum = Project('triquetrum', 'eclipse', 'Triquetrum project', [], ['Triquetrum'], 'None',
                         'bugs.eclipse.org/bugs/xmlrpc.cgi')
    dawnsci = Project('dawnsci', 'eclipse', 'Eclipse DAWNSci™ project', [], ['DAWNsci'], 'None',
                      'bugs.eclipse.org/bugs/xmlrpc.cgi')
    geminiblueprint = Project('gemini.blueprint', 'eclipse', '', [], ['Gemini.Blueprint'], 'None',
                               'bugs.eclipse.org/bugs/xmlrpc.cgi')
    sapphire = Project('sapphire', 'eclipse', 'Sapphire project repository (sapphire)', [], ['Sapphire'], 'None',
                       'bugs.eclipse.org/bugs/xmlrpc.cgi')
    xtextweb = Project('xtext-web', 'eclipse', 'xtext-web', [], ['Web Tools'], 'None',
                       'bugs.eclipse.org/bugs/xmlrpc.cgi')
    qvto = Project('qvto', 'eclipse', 'Model-to-Model Transformation (MMT) project repository (qvto)', [], ['QVTo'],
                   'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    eavp = Project('eavp', 'eclipse', 'Eclipse advanced visualization project', [], ['Eavp'], 'None',
                   'bugs.eclipse.org/bugs/xmlrpc.cgi')
    chemclipse = Project('chemclipse', 'eclipse', 'ChemClipse Project', [], ['Chemclipse'], 'None',
                         'bugs.eclipse.org/bugs/xmlrpc.cgi')
    ecoretools = Project('ecoretools', 'eclipse', 'Ecore Tools project repository (ecoretools)', [], ['Ecoretools'],
                         'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    rdf4jtools = Project('rdf4j-tools', 'eclipse', 'RDF4J Server and Console', [], ['Tools'], 'None',
                         'bugs.eclipse.org/bugs/xmlrpc.cgi')
    libra = Project('libra', 'eclipse', 'Libra project repository (libra)', [], ['Libra'], 'None',
                    'bugs.eclipse.org/bugs/xmlrpc.cgi')
    cft = Project('cft', 'eclipse', '', [], ['CFT'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    tcf = Project('tcf', 'eclipse', 'Target Communication Framework project repository (tcf)', [], ['TCF'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    uomo = Project('uomo', 'eclipse', 'Eclipse UOMo project repository (uomo)', [], ['UOMo'], 'None',
                   'bugs.eclipse.org/bugs/xmlrpc.cgi')
    bpel = Project('bpel', 'eclipse', 'BPEL Designer project repository (bpel)', [], ['BPEL'], 'None',
                   'bugs.eclipse.org/bugs/xmlrpc.cgi')
    osee = Project('osee', 'eclipse', 'Open System Engineering Environment project repository (osee)', [], ['OSEE'],
                   'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    tiakijava = Project('tiaki-java', 'eclipse', 'Tiaki Java projects', [], ['Java Server Faces'], 'None',
                        'bugs.eclipse.org/bugs/xmlrpc.cgi')
    eef = Project('eef', 'eclipse', 'Extended Editing Framework (EEF) project repository (eef)', [], ['EEF'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    windowbuilder = Project('windowbuilder', 'eclipse', 'Windowbuilder', [], ['WindowBuilder'], 'None',
                            'bugs.eclipse.org/bugs/xmlrpc.cgi')
    mylyn = Project('mylyn', 'eclipse', 'Mylyn project repository (mylyn)', [],
                    ['Mylyn', 'Mylyn Commons', 'Mylyn Docs Vex', 'Mylyn Versions', 'Mylyn Reviews', 'Mylyn Tasks',
                     'Mylyn Context MFT', 'Mylyn Docs', 'Mylyn Context', 'Mylyn Builds', 'Mylyn Docs Intent',
                     'Mylyn Reviews R4E', 'Mylyn Incubator'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    geminijpa = Project('gemini.jpa', 'eclipse', 'Gemini JPA project repository (gemini.jpa)', [], ['Gemini.JPA'],
                         'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    riena = Project('riena', 'eclipse', 'Riena Project project repository (riena)', [], ['Riena'], 'None',
                    'bugs.eclipse.org/bugs/xmlrpc.cgi')
    objectteams = Project('objectteams', 'eclipse', 'Object Teams project repository (objectteams)', [],
                          ['Objectteams'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    skalli = Project('skalli', 'eclipse', 'Skalli project repository (skalli)', [], ['Skalli'], 'None',
                     'bugs.eclipse.org/bugs/xmlrpc.cgi')
    gmfruntime = Project('gmf-runtime', 'eclipse', 'modeling.gmp.gmf-runtime project repository', [], ['GMF-Runtime'],
                         'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    egitpde = Project('egit-pde', 'eclipse', 'Eclipse Git Team Provider (EGit) project repository (egit-pde)', [],
                      ['PDE'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    kitalpha = Project('kitalpha', 'eclipse', '', [], ['Kitalpha'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    scanning = Project('scanning', 'eclipse',
                       'Scanning is an open source project for moving scientific instruments and writing NeXus (http://www.nexusformat.org/) compliant files. It is designed to be control system neutral, EPICS, TANGO etc. may be used. See https://projects.eclipse.org/proposals/scanning and https://github.com/eclipse/scanning/blob/master/GETTINGSTARTED.pdf',
                       [], ['Scanning'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    gef3d = Project('gef3d', 'eclipse', 'Graphical Editing Framework 3D project repository (gef3d)', [], ['GEF3D'],
                    'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    virgokerneltools = Project('virgo.kernel-tools', 'eclipse',
                                'Dynamic Enterprise Application Platform project repository (virgo.kernel-tools)', [],
                                ['Tools'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    packager = Project('packager', 'eclipse', 'Eclipse Packager project', [], ['Packager'], 'None',
                       'bugs.eclipse.org/bugs/xmlrpc.cgi')
    capellatools = Project('capella-tools', 'eclipse', '', [], ['Tools'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    gemininaming = Project('gemini.naming', 'eclipse', 'Gemini Naming project repository (gemini.naming)', [],
                            ['Gemini.Naming'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    lyo = Project('lyo', 'eclipse', 'Lyo Project', [], ['Lyo'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    agileuml = Project('agileuml', 'eclipse', '', [], ['Agileuml'], 'None', 'bugs.eclipse.org/bugs/xmlrpc.cgi')
    rtp = Project('rtp', 'eclipse', 'Runtime Packaging project repository (rtp)', [], ['RTP'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')
    incubator = Project('incubator', 'eclipse', 'An eclipse.org repository named incubator', [], ['Incubator'], 'None',
                        'bugs.eclipse.org/bugs/xmlrpc.cgi')
    cdt = Project('cdt', 'eclipse-cdt', 'C/C++ Development Tooling (CDT) Eclipse plug-ins', [], ['CDT'], 'None',
                  'bugs.eclipse.org/bugs/xmlrpc.cgi')

    # BAD PROJECTS - NOT ENOUGH ISSUES
    commonsfileupload = Project('commons-fileupload', 'apache', 'Mirror of Apache Commons FileUpload', ['FILEUPLOAD'],
                                [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    servicemix = Project('servicemix', 'apache', 'Apache ServiceMix', ['SM'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    tomcatmavenplugin = Project('tomcat-maven-plugin', 'apache', 'Mirror of Apache Tomcat Maven plugin', ['MTOMCAT'],
                                [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorcrail = Project('incubator-crail', 'apache', 'Mirror of Apache crail (Incubating)', ['CRAIL'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    stanbol = Project('stanbol', 'apache', 'Mirror of Apache Stanbol (incubating)', ['STANBOL'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonslogging = Project('commons-logging', 'apache', 'Apache Commons Logging', ['LOGGING'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    nifiminifi = Project('nifi-minifi', 'apache', 'Apache MiNiFi (a subproject of Apache NiFi)', ['MINIFI'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    rya = Project('rya', 'apache', 'Mirror of Apache Rya', ['RYA'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticwhirr = Project('attic-whirr', 'apache', 'Mirror of Apache Whirr', ['WHIRR'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    aries = Project('aries', 'apache', 'Apache Aries', ['ARIES'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatoratlas = Project('incubator-atlas', 'apache', 'Mirror of Apache Atlas (Incubating)', ['ATLAS'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    reef = Project('reef', 'apache', 'Mirror of Apache REEF', ['REEF'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    hadoopmapreduce = Project('hadoop-mapreduce', 'apache', 'Mirror of Apache Hadoop MapReduce', ['MAPREDUCE'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    nifiregistry = Project('nifi-registry', 'apache', 'Apache NiFi Registry', ['NIFIREG'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatortuweni = Project('incubator-tuweni', 'apache',
                              'Apache Tuweni is a set of libraries and other tools to aid development of blockchain and other decentralized software in Java and other JVM languages. It includes a low-level bytes library, serialization and deserialization codecs (e.g. RLP), various cryptography functions and primatives, and lots of other helpful utilities.',
                              ['TUWENI'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatornemo = Project('incubator-nemo', 'apache',
                            'Apache Nemo (Incubating) - Data Processing System for Flexible Employment With Different Deployment Characteristics',
                            ['NEMO'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    directoryserver = Project('directory-server', 'apache', 'Apache Directory Server', ['JAMES', 'TS'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    chukwa = Project('chukwa', 'apache', 'Mirror of Apache Chukwa', ['CHUKWA'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    datafu = Project('datafu', 'apache', 'Mirror of Apache DataFu', ['DATAFU'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonscrypto = Project('commons-crypto', 'apache', 'Mirror of Apache Commons Crypto', ['CRYPTO'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    commonsexec = Project('commons-exec', 'apache', 'Apache Commons Exec', ['EXEC'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsjcs = Project('commons-jcs', 'apache', 'Apache Commons JCS', ['JCS'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    sis = Project('sis', 'apache', 'Mirror of Apache SIS', ['SIS'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    ctakes = Project('ctakes', 'apache', 'Mirror of Apache CTakes', ['CTAKES'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    manifoldcf = Project('manifoldcf', 'apache', 'Mirror of Apache ManifoldCF', ['CONNECTORS'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    phoenixomid = Project('phoenix-omid', 'apache', 'Mirror of Apache Omid Incubator', ['OMID'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorhop = Project('incubator-hop', 'apache', 'Hop Orchestration Platform', ['HOP'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    harmony = Project('harmony', 'apache', 'Mirror of Apache Harmony', ['HARMONY'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatortez = Project('incubator-tez', 'apache', 'Mirror of Apache Tez (Incubating)', ['TEZ'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsognl = Project('commons-ognl', 'apache', 'Apache Commons OGNL', ['OGNL'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    directmemory = Project('directmemory', 'apache', 'Mirror of Apache DirectMemory', ['DIRECTMEMORY'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    marmotta = Project('marmotta', 'apache', 'Mirror of Apache Marmotta', ['MARMOTTA'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    commonschain = Project('commons-chain', 'apache', 'Apache Commons Chain', ['CHAIN'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenresolver = Project('maven-resolver', 'apache', 'Apache Maven Artifact Resolver', ['MRESOLVER'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    odftoolkit = Project('odftoolkit', 'apache', 'Apache ODF Toolkit (Incubating) - Project Retired.', ['ODFTOOLKIT'],
                         [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticmrunit = Project('attic-mrunit', 'apache', 'Mirror of Apache MRUnit', ['MRUNIT'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsnumbers = Project('commons-numbers', 'apache', 'Mirror of Apache Commons Numbers', ['NUMBERS'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    clerezza = Project('clerezza', 'apache', 'Mirror of Apache Clerezza', ['CLEREZZA'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorsentry = Project('incubator-sentry', 'apache', 'Mirror of Apache Sentry', ['SENTRY'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjlinkplugin = Project('maven-jlink-plugin', 'apache', 'Apache Maven JLink Plugin', ['MJLINK'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    synapse = Project('synapse', 'apache',
                      'Apache Synapse is a lightweight and high-performance Enterprise Service Bus (ESB)', ['SYNAPSE'],
                      [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsdigester = Project('commons-digester', 'apache', 'Apache Commons Digester', ['DIGESTER'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    opennlpsandbox = Project('opennlp-sandbox', 'apache', 'Mirror of Apache OpenNLP Sandbox',
                             ['SB', 'SANDBOX', 'VELOCITYSB', 'TILESSB'], [], 'http://issues.apache.org/jira',
                             'bz.apache.org/bugzilla/xmlrpc.cgi')
    velocitytools = Project('velocity-tools', 'apache', 'Mirror of Apache Velocity Tools', ['VELTOOLS', 'TOOLS'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    bval = Project('bval', 'apache', 'Mirror of Apache Bean Validation', ['BVAL'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimo = Project('geronimo', 'apache', 'Mirror of Apache Geronimo', ['GERONIMO'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsrdf = Project('commons-rdf', 'apache', 'Mirror of Apache CommonsRDF', ['COMMONSRDF'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ace = Project('ace', 'apache', 'Mirror of Apache ACE (incubating)', ['ACE'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    brooklynserver = Project('brooklyn-server', 'apache', 'Apache Brooklyn Server', ['JAMES', 'TS'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    pivot = Project('pivot', 'apache', 'Mirror of Apache Pivot', ['PIVOT'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjarplugin = Project('maven-jar-plugin', 'apache', 'Apache Maven JAR Plugin', ['MJAR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    phoenixconnectors = Project('phoenix-connectors', 'apache', 'Apache Phoenix Connectors', ['CONNECTORS'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    xalanj = Project('xalan-j', 'apache', 'Mirror of Apache Xalan Java', ['XERCESJ'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatortajo = Project('incubator-tajo', 'apache', 'Mirror of Apache Tajo', ['TAJO'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsscxml = Project('commons-scxml', 'apache', 'Mirror of Apache Commons SCXML', ['SCXML'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsrng = Project('commons-rng', 'apache', 'Mirror of Apache Commons RNG', ['RNG'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticwink = Project('attic-wink', 'apache', 'Apache Wink (Retired)', ['WINK'], [], 'http://issues.apache.org/jira',
                        'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavencleanplugin = Project('maven-clean-plugin', 'apache', 'Apache Maven Clean Plugin', ['MCLEAN'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ddlutils = Project('ddlutils', 'apache', 'Mirror of Apache DB DdlUtils', ['DDLUTILS'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsproxy = Project('commons-proxy', 'apache', 'Apache Commons Proxy', ['PROXY'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jameshupa = Project('james-hupa', 'apache', 'Apache James hupa', ['HUPA'], [], 'http://issues.apache.org/jira',
                        'bz.apache.org/bugzilla/xmlrpc.cgi')
    vxquery = Project('vxquery', 'apache', 'Mirror of Apache VXQuery', ['VXQUERY'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    directoryscimple = Project('directory-scimple', 'apache', 'Apache Directory SCIMple', ['SCIMPLE'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsstatistics = Project('commons-statistics', 'apache', 'Mirror of Apache Commons Statistics', ['STATISTICS'],
                                [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    lenya = Project('lenya', 'apache', 'Mirror of Apache Lenya', [], ['Lenya'], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    cocoon = Project('cocoon', 'apache', 'Mirror of Apache Cocoon', ['COCOON'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    abdera = Project('abdera', 'apache', 'Mirror of Apache Abdera', ['ABDERA'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamesjdkim = Project('james-jdkim', 'apache', 'Mirror of Apache James jdkim', ['JDKIM'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    etch = Project('etch', 'apache', 'Mirror of Apache Etch', ['ETCH'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsjxpath = Project('commons-jxpath', 'apache', 'Apache Commons JXPath', ['JXPATH'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenresourcesplugin = Project('maven-resources-plugin', 'apache', 'Apache Maven Resources Plugin', ['MRESOURCES'],
                                   [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsweaver = Project('commons-weaver', 'apache', 'Apache Commons Weaver', ['WEAVER'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    nifimaven = Project('nifi-maven', 'apache', 'Apache NiFi NAR Maven Plugin', ['MNG'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsgeometry = Project('commons-geometry', 'apache', 'Apache Commons Geometry', ['GEOMETRY'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsbsf = Project('commons-bsf', 'apache', 'Apache Commons BSF', ['BSF'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    xmlgraphicscommons = Project('xmlgraphics-commons', 'apache', 'Mirror of Apache XML Graphics Commons',
                                 ['WSCOMMONS', 'MFCOMMONS', 'XMLCOMMONS'], [], 'http://issues.apache.org/jira',
                                 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamesjspf = Project('james-jspf', 'apache', 'Mirror of Apache James jSPF', ['JSPF'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorbatchee = Project('incubator-batchee', 'apache', 'Mirror of Apache BatchEE', ['BATCHEE'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsfunctor = Project('commons-functor', 'apache', 'Apache Commons Functor', ['FUNCTOR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    maven2 = Project('maven-2', 'apache', 'Mirror of Apache Maven 2', ['LOG4J2', 'WW', 'JS2'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    ignite3 = Project('ignite-3', 'apache', 'Apache Ignite 3', ['COCOON3'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    directorymavibot = Project('directory-mavibot', 'apache', 'Apache Directory Mavibot', ['MAVIBOT'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenhelpplugin = Project('maven-help-plugin', 'apache', 'Apache Maven Help Plugin', ['MPH'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    maveninstallplugin = Project('maven-install-plugin', 'apache', 'Apache Maven Install Plugin', ['MINSTALL'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    creadurrat = Project('creadur-rat', 'apache', 'Apache Creadur - RAT', ['RAT'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    camelkaraf = Project('camel-karaf', 'apache', 'Apache Camel Karaf support', ['KARAF'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenplugintesting = Project('maven-plugin-testing', 'apache', 'Apache Maven Plugin Testing', ['MPLUGINTESTING'],
                                 [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    accumulotesting = Project('accumulo-testing', 'apache', 'Apache Accumulo Testing', ['TESTING'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenscmpublishplugin = Project('maven-scm-publish-plugin', 'apache', 'Apache Maven SCM Publish Plugin',
                                    ['MSCMPUB'], [], 'http://issues.apache.org/jira',
                                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    minavysper = Project('mina-vysper', 'apache', 'Apache Mina Vysper', ['VYSPER'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenchangelogplugin = Project('maven-changelog-plugin', 'apache', 'Apache Maven Changelog Plugin', ['MCHANGELOG'],
                                   [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    chainsaw = Project('chainsaw', 'apache', 'Mirror of Apache Chainsaw', ['CHAINSAW'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    openejb = Project('openejb', 'apache', 'Mirror of Apache OpenEJB', ['OPENEJB'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenantrunplugin = Project('maven-antrun-plugin', 'apache', 'Apache Maven AntRun Plugin', ['MANTRUN'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    brooklyndocs = Project('brooklyn-docs', 'apache', 'Mirror of Apache Brooklyn docs', ['MYNEWTDOC'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavengpgplugin = Project('maven-gpg-plugin', 'apache', 'Apache Maven GPG Plugin', ['MGPG'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    antivyde = Project('ant-ivyde', 'apache', 'Mirror of Apache Ivy Eclipse Plugin', ['IVYDE'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    cayennemodeler = Project('cayenne-modeler', 'apache', 'Mirror of Apache Cayenne Modeler UI', ['MODELER'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfacesextcdi = Project('myfaces-extcdi', 'apache', 'Apache MyFaces ExtCDI (CODI)', ['EXTCDI'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjmodplugin = Project('maven-jmod-plugin', 'apache', 'Apache Maven JMod Plugin', ['MJMOD'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    click = Project('click', 'apache', 'Mirror of Apache Click', ['CLK'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    servicemixcomponents = Project('servicemix-components', 'apache', 'Mirror of Apache ServiceMix components',
                                   ['ZETACOMP', 'EXLBR', 'SMXCOMP'], [], 'http://issues.apache.org/jira',
                                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    ambariinfra = Project('ambari-infra', 'apache', 'Apache Ambari subproject - Infra', ['INFRA'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenjdepsplugin = Project('maven-jdeps-plugin', 'apache', 'Apache Maven JDeps Plugin', ['MJDEPS'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsjelly = Project('commons-jelly', 'apache', 'Apache Commons Jelly', ['JELLY'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsjci = Project('commons-jci', 'apache', 'Apache Commons JCI', ['JCI'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    chemistry = Project('chemistry', 'apache', 'Mirror of Apache Chemistry (incubating)', ['CMIS'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsreleaseplugin = Project('commons-release-plugin', 'apache', 'Mirror of Apache Commons', ['MRELEASE'], [],
                                   'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamesjsieve = Project('james-jsieve', 'apache', 'Mirror of Apache James jSieve', ['JSIEVE'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tilesrequest = Project('tiles-request', 'apache', 'Mirror of Apache Tiles Request', ['TREQ'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    uimasandbox = Project('uima-sandbox', 'apache', 'Mirror of Apache UIMA sandbox',
                          ['SB', 'SANDBOX', 'VELOCITYSB', 'TILESSB'], [], 'http://issues.apache.org/jira',
                          'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenpdfplugin = Project('maven-pdf-plugin', 'apache', 'Apache Maven PDF Plugin', ['MPDF'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    kalumet = Project('kalumet', 'apache', 'Mirror of Apache Kalument (Incubating)', ['KALUMET'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    maventoolchainsplugin = Project('maven-toolchains-plugin', 'apache', 'Apache Maven Toolchains Plugin',
                                    ['MTOOLCHAINS'], [], 'http://issues.apache.org/jira',
                                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    activemqclitools = Project('activemq-cli-tools', 'apache', 'Mirror of Apache ActiveMQ CLI Tools', ['AMQCLI'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    wookie = Project('wookie', 'apache', 'Mirror of Apache Wookie', ['WOOKIE'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenstageplugin = Project('maven-stage-plugin', 'apache', 'Apache Maven Stage Plugin', ['MSTAGE'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavensandbox = Project('maven-sandbox', 'apache', '[deprecated] Mirror of Apache Maven sandbox',
                           ['SB', 'SANDBOX', 'VELOCITYSB', 'TILESSB'], [], 'http://issues.apache.org/jira',
                           'bz.apache.org/bugzilla/xmlrpc.cgi')
    pulsarconnectors = Project('pulsar-connectors', 'apache', 'Apache Pulsar Connectors', ['CONNECTORS'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    dbjdo = Project('db-jdo', 'apache', 'Apache db JDO', ['JDO'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    loggingchainsaw = Project('logging-chainsaw', 'apache', 'Mirror of Apache Chainsaw', ['CHAINSAW'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    activemqopenwire = Project('activemq-openwire', 'apache', 'Mirror of Apache ActiveMQ OpenWire', ['OPENWIRE'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tilesautotag = Project('tiles-autotag', 'apache', 'Mirror of Apache Tiles Autotag', ['AUTOTAG'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    strutssandbox = Project('struts-sandbox', 'apache', 'Mirror of Apache Struts Sandbox',
                            ['SB', 'SANDBOX', 'VELOCITYSB', 'TILESSB'], [], 'http://issues.apache.org/jira',
                            'bz.apache.org/bugzilla/xmlrpc.cgi')
    servicemix4nmr = Project('servicemix4-nmr', 'apache', 'Mirror of Apache Servicemix 4 NMR', ['SMX4NMR'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jsecurity = Project('jsecurity', 'apache', 'Mirror of Apache JSecurity (incubating)', ['JSEC'], [],
                        'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenejbplugin = Project('maven-ejb-plugin', 'apache', 'Apache Maven EJB Plugin', ['MEJB'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    wsaxiom = Project('ws-axiom', 'apache', 'Apache Web Services - Axiom', ['AXIOM'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    kandula = Project('kandula', 'apache', 'Mirror of Apache Kandula', ['KAND'], [], 'http://issues.apache.org/jira',
                      'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorknox = Project('incubator-knox', 'apache', 'Mirror of Apache Knox (Incubating)', ['KNOX'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    servicemix4kernel = Project('servicemix4-kernel', 'apache', 'Mirror of Apache Servicemix 4 kernel', ['SMX4KNL'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    karafjclouds = Project('karaf-jclouds', 'apache', 'Apache jClouds Karaf', ['JCLOUDS'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavendoxiatools = Project('maven-doxia-tools', 'apache', '[deprecated] Mirror of Apache Maven Doxia tools',
                              ['DOXIATOOLS'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonstesting = Project('commons-testing', 'apache', 'Mirror of Apache Commons Testing', ['TESTING'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenverifierplugin = Project('maven-verifier-plugin', 'apache', 'Apache Maven Verifier Plugin', ['MVERIFIER'], [],
                                  'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    turbinecore = Project('turbine-core', 'apache', 'Mirror of Apache Turbine Core', ['MYFACES'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    savan = Project('savan', 'apache', 'Mirror of Apache Savan', ['SAVAN'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimogshell = Project('geronimo-gshell', 'apache', 'Mirror of Apache Geronimo gshell', ['GSHELL'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfacesscripting = Project('myfaces-scripting', 'apache', 'Apache MyFaces Scripting', ['MSCRIPTING'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    creadurtentacles = Project('creadur-tentacles', 'apache', 'Mirror of Apache Tentacles', ['TENTACLES'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenresources = Project('maven-resources', 'apache', '[deprecated] Mirror of Apache Maven resources',
                             ['RESOURCES'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    nuvem = Project('nuvem', 'apache', 'Mirror of Apache Nuvem', ['NUVEM'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    any23server = Project('any23-server', 'apache', 'Apache Any23 Server Project', ['JAMES', 'TS'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    juddiscout = Project('juddi-scout', 'apache', 'Mirror of Apache jUDDI', ['SCOUT'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jcloudslabs = Project('jclouds-labs', 'apache', 'Apache jClouds Labs', ['LABS'], [],
                          'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    sandesha = Project('sandesha', 'apache', 'Mirror of Apache Sandesha', ['SAND'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    wsneethi = Project('ws-neethi', 'apache', 'Apache WebService - Neethi', ['NEETHI'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticodejacob = Project('attic-ode-jacob', 'apache', 'Mirror of Apache Ode Jacob', ['JACOB'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    accumulopig = Project('accumulo-pig', 'apache', 'Apache Accumulo Pig', ['PIG'], [], 'http://issues.apache.org/jira',
                          'bz.apache.org/bugzilla/xmlrpc.cgi')
    redbackcomponents = Project('redback-components', 'apache', 'Mirror of Apache Redback components',
                                ['ZETACOMP', 'EXLBR', 'SMXCOMP'], [], 'http://issues.apache.org/jira',
                                'bz.apache.org/bugzilla/xmlrpc.cgi')
    mavenruntime = Project('maven-runtime', 'apache', 'Apache Maven Runtime -- Archived', ['RUNTIME'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jackrabbitocm = Project('jackrabbit-ocm', 'apache', 'Mirror of Apache Jackrabbit OCM', ['OCM'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    geronimobatchee = Project('geronimo-batchee', 'apache', 'Apache Geronimo BatchEE JBatch implementation',
                              ['BATCHEE'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    myfacestest = Project('myfaces-test', 'apache', 'Apache MyFaces test framework', ['MXNETTEST', 'MYFACESTEST'],
                          ['Test'], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    tomeepatchplugin = Project('tomee-patch-plugin', 'apache', 'Apache TomEE Patch Plugin', ['MPATCH'], [],
                               'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    archivacomponents = Project('archiva-components', 'apache', 'Components used by Apache Archiva and Redback',
                                ['ZETACOMP', 'EXLBR', 'SMXCOMP'], [], 'http://issues.apache.org/jira',
                                'bz.apache.org/bugzilla/xmlrpc.cgi')
    dubbo = Project('dubbo', 'apache', 'Apache Dubbo is a high-performance, java based, open source RPC framework.',
                    ['DUBBO'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    rocketmq = Project('rocketmq', 'apache', 'Mirror of Apache RocketMQ', ['ROCKETMQ'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    pulsar = Project('pulsar', 'apache', 'Apache Pulsar - distributed pub-sub messaging system', ['PULSAR'], [],
                     'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    hbase = Project('hbase', 'apache', 'Apache HBase', ['HBASE'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorpinot = Project('incubator-pinot', 'apache',
                             'Apache Pinot (Incubating) - A realtime distributed OLAP datastore', ['PINOT'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorgobblin = Project('incubator-gobblin', 'apache',
                               'A distributed data integration framework that simplifies common aspects of big data integration such as data ingestion, replication, organization and lifecycle management for both streaming and batch data ecosystems.',
                               ['GOBBLIN'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    netbeans = Project('netbeans', 'apache', 'Apache NetBeans', ['NETBEANS'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    usergrid = Project('usergrid', 'apache', 'Mirror of Apache Usergrid', ['USERGRID'], [],
                       'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    cloudstack = Project('cloudstack', 'apache', 'Apache Cloudstack', ['CLOUDSTACK'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorsedona = Project('incubator-sedona', 'apache',
                              'A cluster computing framework for processing large-scale geospatial data', ['SEDONA'],
                              [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    sqoop = Project('sqoop', 'apache', 'Mirror of Apache Sqoop', ['SQOOP'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    mina = Project('mina', 'apache', 'Mirror of Apache MINA', ['DIRMINA'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    griffin = Project('griffin', 'apache', 'Mirror of Apache griffin ', ['GRIFFIN'], [],
                      'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    atticaurora = Project('attic-aurora', 'apache',
                          'Apache Aurora - A Mesos framework for long-running services, cron jobs, and ad-hoc jobs',
                          ['AURORA'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    freemarker = Project('freemarker', 'apache', 'Apache Freemarker', ['FREEMARKER'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    giraph = Project('giraph', 'apache', 'Mirror of Apache Giraph', ['GIRAPH'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    fineract = Project('fineract', 'apache', 'Apache Fineract', ['FINERACT'], [], 'http://issues.apache.org/jira',
                       'bz.apache.org/bugzilla/xmlrpc.cgi')
    servicecombtoolkit = Project('servicecomb-toolkit', 'apache', 'Apache servicecomb', ['ODFTOOLKIT'], [],
                                 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    jamesproject = Project('james-project', 'apache', 'Emails at the heart of your business logic!', ['TST'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    eagle = Project('eagle', 'apache', 'Mirror of Apache Eagle', ['EAGLE'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    bahirflink = Project('bahir-flink', 'apache', 'Mirror of Apache Bahir Flink', ['FLINK'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorratis = Project('incubator-ratis', 'apache',
                             'Open source Java implementation for Raft consensus protocol.', ['RATIS'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    submarine = Project('submarine', 'apache', 'Submarine is Cloud Native Machine Learning Platform.', ['SUBMARINE'],
                        [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    bigtop = Project('bigtop', 'apache', 'Mirror of Apache Bigtop', ['BIGTOP'], [], 'http://issues.apache.org/jira',
                     'bz.apache.org/bugzilla/xmlrpc.cgi')
    tez = Project('tez', 'apache', 'Mirror of Apache Tez', ['TEZ'], [], 'http://issues.apache.org/jira',
                  'bz.apache.org/bugzilla/xmlrpc.cgi')
    ofbizframework = Project('ofbiz-framework', 'apache',
                             'Apache OFBiz is an open source product for the automation of enterprise processes. It includes framework components and business applications for ERP, CRM, E-Business/E-Commerce, Supply Chain Management and Manufacturing Resource Planning. OFBiz provides a foundation and starting point for reliable, secure and scalable enterprise solutions.',
                             ['DBF'], [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatortubemq = Project('incubator-tubemq', 'apache', 'Apache TubeMQ', ['TUBEMQ'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorhivemall = Project('incubator-hivemall', 'apache', 'Mirror of Apache Hivemall (incubating)', ['HIVEMALL'],
                                [], 'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    plc4x = Project('plc4x', 'apache', 'PLC4X The Industrial IoT adapter', ['PLC4X'], [],
                    'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    commonsimaging = Project('commons-imaging', 'apache', 'Mirror of Apache Commons Imaging', ['IMAGING'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    derby = Project('derby', 'apache', 'Mirror of Apache Derby', ['DERBY'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorsamoa = Project('incubator-samoa', 'apache', 'Mirror of Apache Samoa (Incubating)', ['SAMOA'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    dubboproxy = Project('dubbo-proxy', 'apache', 'Apache dubbo', ['PROXY'], [], 'http://issues.apache.org/jira',
                         'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorstreampipes = Project('incubator-streampipes', 'apache',
                                   'Apache StreamPipes - A self-service (Industrial) IoT toolbox to enable non-technical users to connect, analyze and explore IoT data streams.',
                                   ['STREAMPIPES'], [], 'http://issues.apache.org/jira',
                                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    distributedlog = Project('distributedlog', 'apache', 'Apache DistributedLog', ['DL'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    oltu = Project('oltu', 'apache', 'Mirror of Apache Oltu', ['OLTU'], [], 'http://issues.apache.org/jira',
                   'bz.apache.org/bugzilla/xmlrpc.cgi')
    hadoopcommon = Project('hadoop-common', 'apache', 'Mirror of Apache Hadoop common', ['HADOOP'], [],
                           'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatormyriad = Project('incubator-myriad', 'apache', 'Mirror of Apache Myriad (Incubating)', ['MYRIAD'], [],
                              'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    unomi = Project('unomi', 'apache', 'Apache Unomi', ['UNOMI'], [], 'http://issues.apache.org/jira',
                    'bz.apache.org/bugzilla/xmlrpc.cgi')
    activemqapollo = Project('activemq-apollo', 'apache', 'Mirror of Apache ActiveMQ Apollo', ['APLO', 'APOLLO'], [],
                             'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    hadoophdfs = Project('hadoop-hdfs', 'apache', 'Mirror of Apache Hadoop HDFS', ['HDFS'], [],
                         'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    flinktraining = Project('flink-training', 'apache', 'Apache Flink Training Excercises', ['TRAINING'], [],
                            'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')
    incubatorbrooklyn = Project('incubator-brooklyn', 'apache', 'Mirror of Apache Brooklyn', ['BROOKLYN'], [],
                                'http://issues.apache.org/jira', 'bz.apache.org/bugzilla/xmlrpc.cgi')

    springframework = Project('spring-framework', 'spring-projects', 'Spring Framework', ['SPR'], [],
                              'https://jira.spring.io', 'None')
    springsecurity = Project('spring-security', 'spring-projects', 'Spring Security', ['SEC'], [],
                             'https://jira.spring.io', 'None')
    springsecurityoauth = Project('spring-security-oauth', 'spring-projects',
                                  'Support for adding OAuth1(a) and OAuth2 features (consumer and provider) for Spring web applications.',
                                  ['SECOAUTH'], [], 'https://jira.spring.io', 'None')
    springdataelasticsearch = Project('spring-data-elasticsearch', 'spring-projects',
                                      'Provide support to increase developer productivity in Java when using Elasticsearch. Uses familiar Spring concepts such as a template classes for core API usage and lightweight repository style data access.',
                                      ['DATAES'], [], 'https://jira.spring.io', 'None')
    springdatajpa = Project('spring-data-jpa', 'spring-projects',
                            'Simplifies the development of creating a JPA-based data access layer. ', ['DATAJPA'], [],
                            'https://jira.spring.io', 'None')
    springintegrationsamples = Project('spring-integration-samples', 'spring-projects',
                                       'You are looking for examples, code snippets, sample applications for Spring Integration? This is the place.',
                                       ['INTSAMPLES'], [], 'https://jira.spring.io', 'None')
    springbatch = Project('spring-batch', 'spring-projects',
                          'Spring Batch is a framework for writing offline and batch applications using Spring and Java',
                          ['BATCH'], [], 'https://jira.spring.io', 'None')
    greenhouse = Project('greenhouse', 'spring-projects',
                         'Reference web application for Spring technologies and social destination for Spring developers.',
                         ['GREENHOUSE'], [], 'https://jira.spring.io', 'None')
    springdataredis = Project('spring-data-redis', 'spring-projects',
                              'Provides support to increase developer productivity in Java when using Redis, a key-value store. Uses familiar Spring concepts such as a template classes for core API usage and lightweight repository style data access.',
                              ['DATAREDIS'], [], 'https://jira.spring.io', 'None')
    springdatamongodb = Project('spring-data-mongodb', 'spring-projects',
                                'Provide support to increase developer productivity in Java when using MongoDB. Uses familiar Spring concepts such as a template classes for core API usage and lightweight repository style data access.',
                                ['DATAMONGO'], [], 'https://jira.spring.io', 'None')
    springintegration = Project('spring-integration', 'spring-projects',
                                'Spring Integration provides an extension of the Spring programming model to support the well-known Enterprise Integration Patterns (EIP)',
                                ['INT'], [], 'https://jira.spring.io', 'None')
    springdatarest = Project('spring-data-rest', 'spring-projects',
                             'Simplifies building hypermedia-driven REST web services on top of Spring Data repositories',
                             ['DATAREST'], [], 'https://jira.spring.io', 'None')
    springandroid = Project('spring-android', 'spring-projects',
                            'Support for Springs RestTemplate within native Android applications', ['ANDROID'], [],
                            'https://jira.spring.io', 'None')
    springroo = Project('spring-roo', 'spring-projects',
                        'Spring Roo is a next-generation rapid application development tool for Java developers. It focuses on higher productivity, stock-standard Java APIs, high usability, avoiding engineering trade-offs and facilitating easy Roo removal.',
                        ['ROO'], [], 'https://jira.spring.io', 'None')
    springdataneo4j = Project('spring-data-neo4j', 'spring-projects',
                              'Provide support to increase developer productivity in Java when using Neo4j. Uses familiar Spring concepts such as a template classes for core API usage and lightweight repository style data access.',
                              ['DATAGRAPH'], [], 'https://jira.spring.io', 'None')
    springamqp = Project('spring-amqp', 'spring-projects',
                         'Spring AMQP - support for Spring programming model with AMQP, especially but not limited to RabbitMQ',
                         ['AMQP'], [], 'https://jira.spring.io', 'None')
    springsocial = Project('spring-social', 'spring-projects',
                           'Allows you to connect your applications with SaaS providers such as Facebook and Twitter.',
                           ['SPRNETSOCIAL', 'SOCIAL'], [], 'https://jira.spring.io', 'None')
    springdatacommons = Project('spring-data-commons', 'spring-projects',
                                'Spring Data Commons. Interfaces and code shared between the various datastore specific implementations.',
                                ['DATACMNS'], [], 'https://jira.spring.io', 'None')
    springxd = Project('spring-xd', 'spring-projects',
                       'Spring XD makes it easy to solve common big data problems such as data ingestion and export, real-time analytics, and batch workflow orchestration',
                       ['XD'], [], 'https://jira.spring.io', 'None')
    springshell = Project('spring-shell', 'spring-projects', 'Spring based interactive shell', ['SHL'], [],
                          'https://jira.spring.io', 'None')
    restshell = Project('rest-shell', 'spring-projects',
                        'Command-line shell for interacting with Spring HATEOAS-compliant REST resources', ['SHL'], [],
                        'https://jira.spring.io', 'None')
    springdatajdbc = Project('spring-data-jdbc', 'spring-projects', 'Spring Data JDBC', ['DATAJDBC'], [],
                             'https://jira.spring.io', 'None')
    springide = Project('spring-ide', 'spring-projects', 'Spring Development Environment for Eclipse', ['IDE'], [],
                        'https://jira.spring.io', 'None')
    springldap = Project('spring-ldap', 'spring-projects', 'Spring LDAP', ['LDAP'], [], 'https://jira.spring.io',
                         'None')
    springintegrationextensions = Project('spring-integration-extensions', 'spring-projects',
                                          'The Spring Integration Extensions project provides extension components for Spring Integration',
                                          ['INTEXT'], [], 'https://jira.spring.io', 'None')
    springsocialfacebook = Project('spring-social-facebook', 'spring-projects',
                                   'Facebook API binding and connect support.', ['SPRNETSOCIALFB', 'SOCIALFB'], [],
                                   'https://jira.spring.io', 'None')
    springdatacouchbase = Project('spring-data-couchbase', 'spring-projects', 'Spring Data Couchbase', ['DATACOUCH'],
                                  [], 'https://jira.spring.io', 'None')
    springmobile = Project('spring-mobile', 'spring-projects',
                           'Extensions to Spring MVC for developing mobile web applications.', ['MOBILE'], [],
                           'https://jira.spring.io', 'None')
    grailsdatamapping = Project('grails-data-mapping', 'spring-projects', 'Grails Data Mapping Project', ['DATAMAP'],
                                [], 'https://jira.spring.io', 'None')
    springsocialtwitter = Project('spring-social-twitter', 'spring-projects',
                                  'Twitter API binding and connect support.', ['SPRNETSOCIALTW', 'SOCIALTW'], [],
                                  'https://jira.spring.io', 'None')
    springdatagemfire = Project('spring-data-gemfire', 'spring-projects', 'Spring Data integration for Pivotal GemFire',
                                ['SGF'], [], 'https://jira.spring.io', 'None')
    springsocialgithub = Project('spring-social-github', 'spring-projects', 'Github API binding and connect support.',
                                 ['SOCIALGH'], [], 'https://jira.spring.io', 'None')
    springdatakeyvalue = Project('spring-data-keyvalue', 'spring-projects',
                                 'Project to provide infrastructure to implement Spring Data repositories on top of key-value-based, in-memory data stores.',
                                 ['DATAKV'], [], 'https://jira.spring.io', 'None')
    springsociallinkedin = Project('spring-social-linkedin', 'spring-projects',
                                   'LinkedIn API binding and connect support.', ['SPRNETSOCIALLI', 'SOCIALLI'], [],
                                   'https://jira.spring.io', 'None')
    greenhouseandroid = Project('greenhouse-android', 'spring-projects', 'Greenhouse native Android client',
                                ['ANDROID'], [], 'https://jira.spring.io', 'None')
    springdataldap = Project('spring-data-ldap', 'spring-projects', 'Repository abstraction for Spring LDAP',
                             ['DATALDAP'], [], 'https://jira.spring.io', 'None')
    springdatageode = Project('spring-data-geode', 'spring-projects', 'Spring Data support for Apache Geode',
                              ['DATAGEODE'], [], 'https://jira.spring.io', 'None')
    springmigrationanalyzer = Project('spring-migration-analyzer', 'spring-projects',
                                      'Spring Migration Anaylzer is a command-line tool for analyzing Java EE applications. It produces a report describing the application and how to migrate it to Spring.',
                                      ['SMA'], [], 'https://jira.spring.io', 'None')
    grailside = Project('grails-ide', 'spring-projects', 'Grails Developer Tooling for Eclipse', ['IDE'], [],
                        'https://jira.spring.io', 'None')
    springsocialtripit = Project('spring-social-tripit', 'spring-projects', 'TripIt API binding and connect support.',
                                 ['SOCIALTI'], [], 'https://jira.spring.io', 'None')


def get_good_projects():
    GOOD = ['kafka', 'flink', 'hadoop', 'zookeeper', 'cassandra', 'storm', 'tomcat', 'zeppelin', 'jmeter', 'beam', 'lucenesolr', 'groovy', 'ignite', 'camel', 'hive', 'shiro', 'kylin', 'curator', 'nifi', 'maven', 'calcite', 'nutch', 'commonslang', 'flume', 'mahout', 'geode', 'activemq', 'avro', 'hudi', 'drill', 'ambari', 'pdfbox', 'tinkerpop', 'tika', 'bookkeeper', 'poi', 'logginglog4j2', 'iotdb', 'opennlp', 'phoenix', 'accumulo', 'systemds', 'metron', 'commonsio', 'atlas', 'log4j', 'ofbiz', 'jena', 'cxf', 'samza', 'activemqartemis', 'pig', 'oozie', 'isis', 'wicket', 'karaf', 'commonscollections', 'ranger', 'openmeetings', 'commonsmath', 'tomee', 'commonspool', 'minasshd', 'atticapexcore', 'jackrabbitoak', 'mavensurefire', 'helix', 'commonscodec', 'ant', 'archiva', 'commonsdbutils', 'commonsdbcp', 'cayenne', 'commonscsv', 'httpcomponentscore', 'commonscli', 'commonsbeanutils', 'commonstext', 'asterixdb', 'commonscompress', 'atticstratos', 'metamodel', 'commonsbcel', 'commonsnet', 'commonsvfs', 'atticapexmalhar', 'deltaspike', 'hama', 'tajo', 'syncope', 'xmlgraphicsbatik', 'commonsvalidator', 'xmlgraphicsfop', 'commonsconfiguration', 'knox', 'qpid', 'sentry', 'crunch', 'tiles', 'mavenarchetype', 'gora', 'falcon', 'roller', 'jclouds', 'mnemonic', 'openjpa', 'joshua', 'tapestry5', 'commonsjexl', 'commonsemail', 'httpasyncclient', 'mavencompilerplugin', 'airavata', 'jspwiki', 'mavenscm', 'streams', 'directorystudio', 'shindig', 'mavenshadeplugin', 'ftpserver', 'twill', 'mavendependencyplugin', 'juneau', 'myfaces', 'lens', 'hcatalog', 'oodt', 'qpidjms', 'openwebbeans', 'openwebbeansmeecrowave', 'mavenindexer', 'antivy', 'atticode', 'mavenassemblyplugin', 'mavenwagon', 'johnzon', 'xmlbeans', 'sanselan', 'jamesmime4j', 'mavenjavadocplugin', 'jackrabbitfilevault', 'mavencheckstyleplugin', 'cxfdosgi', 'phoenixtephra', 'mavenplugintools', 'empiredb', 'xerces2j', 'mavendeployplugin', 'portalspluto', 'mavendoxia', 'mavenpmdplugin', 'mavenwarplugin', 'cxffediz', 'mavensiteplugin', 'minaftpserver', 'atticrave', 'juddi', 'myfacestobago', 'mavenprojectinforeportsplugin', 'cxfxjcutils', 'mavensourceplugin', 'maveninvokerplugin', 'geronimoxbean', 'wswss4j', 'continuum', 'mavenremoteresourcesplugin', 'mavenearplugin', 'mavenpatchplugin', 'incubatorambari', 'mavenjxr', 'geronimodevtools', 'mavenchangesplugin', 'mavendoxiasitetools', 'mavenrarplugin', 'myfacestrinidad', 'creadurwhisker', 'archivasandbox', 'wsxmlschema', 'accumuloproxy', 'minaasyncweb', 'atticonami', 'geronimoyoko', 'mavendoapplugin', 'mavenjdeprscanplugin', 'incubatortwill', 'jamespostage', 'rampart', 'mavenacrplugin', 'mavenlinkcheckplugin']
    return list(filter(lambda x: x.name in GOOD, ProjectName))

def get_average_years():
    import github3
    gh = github3.login(token=os.environ['GITHUB_TOKEN'])
    years = []
    for p in ProjectName:
        years.append(gh.repository(p.value.github_user, p.value.github_name).created_at.year)

    pass

if __name__ == "__main__":
    # get_average_years()
    ans = ['ping 127.0.0.1 -n 5']
    # for i in range(8):
    # ans.extend(list(map(lambda x: 'gh issue create -t {0} -b skip'.format(x.name), get_good_projects())))
    for p in ProjectName:
        ans.append('gh issue create -t {0} -b "skip" '.format(p.name))
        ans.append('ping 127.0.0.1 -n 10')
    # ans.extend(list(map(lambda x: 'gh issue create -t {0} -b "-a" '.format(x.name), ProjectName)))
    # ans.extend(list(map(lambda x: 'gh issue create -t {0} -b skip'.format(x.name), list(filter(lambda x: x.value.bz_names, ProjectName)))))
    # ans.extend(list(map(lambda x: 'gh issue create -t {0} -b skip'.format(x.name), list(filter(lambda x: x.value.github_user == 'spring-projects', ProjectName)))))
    print("\n".join(ans))
    # print(ans)
    # print(len(ans))