from metrics.version_metrics_data import DataBuilder, CheckstyleData
from metrics.version_metrics_name import DataNameEnum
from projects import ProjectName


class TestDataBuilder:
    @staticmethod
    def get_data_builder():
        return DataBuilder(ProjectName.CommonsLang, "LANG_3_4_RC1")

    @staticmethod
    def add_single_metric(db: DataBuilder) -> DataBuilder:
        db.append(DataNameEnum.NumberOfPublicMethods_Checkstyle)
        return db

    @staticmethod
    def add_multiple_metrics(db: DataBuilder) -> DataBuilder:
        # checkstyle
        db.append(DataNameEnum.ThrowsCount)
        db.append(DataNameEnum.SwissArmyKnife)
        db.append(DataNameEnum.BrokenHierarchy)
        # ck
        db.append(DataNameEnum.WMC_CK)
        # designite design
        db.append(DataNameEnum.ImperativeAbstraction)
        # designite implementation
        db.append(DataNameEnum.ComplexConditional)
        # designite method metrics
        db.append(DataNameEnum.LOCMethod)
        # designite method organic
        db.append(DataNameEnum.LongMethod_Organic)
        # designite type metrics
        db.append(DataNameEnum.NumberOfMethods_Designite)
        # designite type organic
        db.append(DataNameEnum.GodClass)
        # mood
        db.append(DataNameEnum.NumberOfPublicAttributes)
        # halstead
        db.append(DataNameEnum.Length)
        # bugged
        db.append(DataNameEnum.Bugged)
        return db

    '''
    @staticmethod
    def add_multiple_metrics(db: DataBuilder) -> DataBuilder:
        db.append(DataName.ComplexMethod)
        db.append(DataName.CBO)
        db.append(DataName.MultipathHierarchy)
        db.append(DataName.BrokenModularization)
        db.append(DataName.NestedForDepth)
        db.append(DataName.NumberOfPackageMethod)
        db.append(DataName.NumberPublicMethods)
        db.append(DataName.BrokenModularization)
        db.append(DataName.MissingHierarchy)
        return db
    '''

#    def test_data_builder_empty_repr(self):
#        db = self.get_data_builder()
#        assert repr(db) == "Empty"
#
#    def test_data_builder_one_item_repr(self):
#        db = self.get_data_builder()
#        db = self.add_single_metric(db)
#        assert repr(db) == """designite_type_organic\n\tAntiSingleton
#"""
#
#    def test_data_builder_multiple_items_repr(self):
#        db = self.get_data_builder()
#        db = self.add_multiple_metrics(db)
#        assert repr(db) == """designite_implementation
#\tComplexMethod\nck\n\tCBO\ndesignite_design
#\tMultipathHierarchy\n\tBrokenModularization\ncheckstyle
#\tNestedForDepth\n\tNumberOfPackageMethod\nmood
#\tNumberPublicMethods
#"""

    def test_data_builder_one_item_build(self):
        db = self.get_data_builder()
        db = self.add_single_metric(db)
        db.build()

    def test_data_builder_multiple_item_build(self):
        db = self.get_data_builder()
        db = self.add_multiple_metrics(db)
        db.build()

    def test_data_builder_bugged_item(self):
        db = DataBuilder(ProjectName.CommonsLang, "LANG_3_4_RC1")
        db.append(DataNameEnum.Bugged)
        db.build()


class TestCheckstyleData:
    PROJECT = "commons-lang"
    VERSION = "LANG_3_4_RC1"
    DATA_DIMENSION = 5462
    COLUMN_DIMENSION = 22
    RANDOM_POSITION_ONE = (37, 5)
    RANDOM_VALUE_ONE = 21
    RANDOM_POSITION_TWO = (161, 12)
    RANDOM_VALUE_TWO = 25
    DATA_TYPE = "checkstyle"

    def test_checkstyle_data_type(self):
        c = CheckstyleData(ProjectName.CommonsLang.value, TestCheckstyleData.VERSION)
        assert c.data_type == TestCheckstyleData.DATA_TYPE

    def test_checkstyle_data_column_dimension(self):
        c = CheckstyleData(ProjectName.CommonsLang.value, TestCheckstyleData.VERSION)
        assert len(c.data.columns) == TestCheckstyleData.COLUMN_DIMENSION
