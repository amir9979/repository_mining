from metrics.version_metrics import Halstead, Checkstyle, Designite, CK, Mood


class TestExtractor:
    def test_checkstyle(self):
        m = Checkstyle("commons-lang", "LANG_3_4_RC1", "LANG", "tests/commons_lang")
        m.extract()

    def test_designite(self):
        m = Designite("commons-lang", "LANG_3_4_RC1", "LANG", "tests/commons_lang")
        m.extract()

    def test_ck(self):
        m = CK("commons-lang", "LANG_3_4_RC1", "LANG", "tests/commons_lang")
        m.extract()

    def test_mood(self):
        m = Mood("commons-lang", "LANG_3_4_RC1", "LANG", "tests/commons_lang")
        m.extract()

    def test_halstead(self):
        m = Halstead("commons-lang", "LANG_3_4_RC1", "LANG", "tests/commons_lang")
        m.extract()
