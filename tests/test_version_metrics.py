from metrics.version_metrics import Halstead, Checkstyle, Designite, CK, Mood, Bugged, JavaParserFileAnalyser
from projects import ProjectName


class TestExtractor:
    # check repository_mining/repository_data/metrics/commons-lang/LANG_3_4_RC1/**.csv
    def test_bugged(self):
        m = Bugged(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()

    def test_checkstyle(self):
        m = Checkstyle(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()

    def test_designite(self):
        m = Designite(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()

    def test_ck(self):
        m = CK(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()

    def test_mood(self):
        m = Mood(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()

    def test_halstead(self):
        m = Halstead(ProjectName.CommonsLang.value, "LANG_3_4_RC1")
        m.extract()


class TestJavaParserFileAnalyser:
    def test_get_closest_id(self):
        extractor = JavaParserFileAnalyser(
            "/Users/brunomachado/apache_repos/commons-lang",
            "commons-lang",
            "LANG_3_4_RC1")
        extractor.get_closest_id(
            "src/test/java/org/apache/commons/lang3/mutable/MutableDoubleTest.java",
            44)

    def test__get_classes_path(self):
        extractor = JavaParserFileAnalyser(
            "/Users/brunomachado/apache_repos/commons-lang",
            "commons-lang",
            "LANG_3_4_RC1")
        extractor._get_classes_path()

    def test__get_methods_by_path_and_name(self):
        extractor = JavaParserFileAnalyser(
            "/Users/brunomachado/apache_repos/commons-lang",
            "commons-lang",
            "LANG_3_4_RC1")
        extractor._get_methods_by_path_and_name()