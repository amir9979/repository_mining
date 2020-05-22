from metrics.version_metrics import Halstead, Checkstyle, Designite, CK, Mood, Bugged
from projects import ProjectName


class TestExtractor:
    # check repository_mining/repository_data/metrics/commons-lang/LANG_3_4_RC1/**.csv
    def test_bugged(self):
        m = Bugged(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()

    def test_checkstyle(self):
        m = Checkstyle(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()

    def test_designite(self):
        m = Designite(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()

    def test_ck(self):
        m = CK(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()

    def test_mood(self):
        m = Mood(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()

    def test_halstead(self):
        m = Halstead(ProjectName.CommonsLang, "LANG_3_4_RC1")
        m.extract()
