from enum import Enum, auto
from typing import List


class DataType(Enum):
    CheckstyleDataType = "checkstyle"
    DesigniteDesignSmellsDataType = "designite_design"
    DesigniteImplementationSmellsDataType = "designite_implementation"
    DesigniteOrganicTypeSmellsDataType = "designite_type_organic"
    DesigniteOrganicMethodSmellsDataType = "designite_method_organic"
    DesigniteTypeMetricsDataType = "designite_type_metrics"
    DesigniteMethodMetricsDataType = "designite_method_metrics"
    SourceMonitorFilesDataType = "source_monitor_files"
    SourceMonitorDataType = "source_monitor"
    CKDataType = "ck"
    MoodDataType = "mood"
    HalsteadDataType = "halstead"
    BuggedDataType = "bugged"
    BuggedMethodsDataType = "bugged_methods"
    JasomeFilesDataType = "jasome_files"
    JasomeMoodDataType = "jasome_mood"
    JasomeCKDataType = "jasome_ck"
    JasomeLKDataType = "jasome_lk"
    JasomeMethodsDataType = "jasome_methods"
    ProcessFilesDataType = "process_files"
    IssuesFilesDataType = "issues_files"


class DataName:
    def __init__(self, name, data_type: DataType, column_name, description=""):
        self.name = data_type.value + "_" + name
        self.data_type = data_type
        self.data_type_value = data_type.value
        self.column_name = column_name
        self.description = description

    def as_data_dict(self):
        return {'data_value': self.name, 'data_type': self.data_type_value, 'data_column': self.column_name}

    def as_description_dict(self):
        return {"feature_name": self.name, "feature_group": self.data_type_value, "column_name": self.column_name, "description": self.description}


class DataNameEnum(Enum):
    Bugged = DataName("Bugged", DataType.BuggedDataType, "is_buggy")
    BuggedMethods = DataName("BuggedMethods", DataType.BuggedMethodsDataType, "is_method_buggy")

    ImperativeAbstraction = DataName("ImperativeAbstraction", DataType.DesigniteDesignSmellsDataType, "Imperative Abstraction")
    MultifacetedAbstraction = DataName("MultifacetedAbstraction", DataType.DesigniteDesignSmellsDataType, "Multifaceted Abstraction")
    UnnecessaryAbstraction = DataName("UnnecessaryAbstraction", DataType.DesigniteDesignSmellsDataType, "Unnecessary Abstraction")
    UnutilizedAbstraction = DataName("UnutilizedAbstraction", DataType.DesigniteDesignSmellsDataType, "Unutilized Abstraction")
    DeficientEncapsulation = DataName("DeficientEncapsulation", DataType.DesigniteDesignSmellsDataType, "Deficient Encapsulation")
    UnexploitedEncapsulation = DataName("UnexploitedEncapsulation", DataType.DesigniteDesignSmellsDataType, "Unexploited Encapsulation")
    BrokenModularization = DataName("BrokenModularization", DataType.DesigniteDesignSmellsDataType, "Broken Modularization")
    Cyclic_DependentModularization = DataName("Cyclic_DependentModularization", DataType.DesigniteDesignSmellsDataType, "Cyclic-Dependent Modularization")
    InsufficientModularization = DataName("InsufficientModularization", DataType.DesigniteDesignSmellsDataType, "Insufficient Modularization")
    Hub_likeModularization = DataName("Hub_likeModularization", DataType.DesigniteDesignSmellsDataType, "Hub-like Modularization")
    BrokenHierarchy = DataName("BrokenHierarchy", DataType.DesigniteDesignSmellsDataType, "Broken Hierarchy")
    CyclicHierarchy = DataName("CyclicHierarchy", DataType.DesigniteDesignSmellsDataType, "Cyclic Hierarchy")
    DeepHierarchy = DataName("DeepHierarchy", DataType.DesigniteDesignSmellsDataType, "Deep Hierarchy")
    MissingHierarchy = DataName("MissingHierarchy", DataType.DesigniteDesignSmellsDataType, "Missing Hierarchy")
    MultipathHierarchy = DataName("MultipathHierarchy", DataType.DesigniteDesignSmellsDataType, "Multipath Hierarchy")
    RebelliousHierarchy = DataName("RebelliousHierarchy", DataType.DesigniteDesignSmellsDataType, "Rebellious Hierarchy")
    WideHierarchy = DataName("WideHierarchy", DataType.DesigniteDesignSmellsDataType, "Wide Hierarchy")

    AbstractFunctionCallFromConstructor = DataName("AbstractFunctionCallFromConstructor", DataType.DesigniteImplementationSmellsDataType, "Abstract Function Call From Constructor")
    ComplexConditional = DataName("ComplexConditional", DataType.DesigniteImplementationSmellsDataType, "Complex Conditional")
    ComplexMethod = DataName("ComplexMethod", DataType.DesigniteImplementationSmellsDataType, "Complex Method")
    EmptyCatchClause = DataName("EmptyCatchClause", DataType.DesigniteImplementationSmellsDataType, "Empty catch clause")
    LongIdentifier = DataName("LongIdentifier", DataType.DesigniteImplementationSmellsDataType, "Long Identifier")
    LongMethod_Designite = DataName("LongMethod_Designite", DataType.DesigniteImplementationSmellsDataType, "Long Method")
    LongParameterList_Designite = DataName("LongParameterList_Designite", DataType.DesigniteImplementationSmellsDataType, "Long Parameter List")
    LongStatement = DataName("LongStatement", DataType.DesigniteImplementationSmellsDataType, "Long Statement")
    MagicNumber = DataName("MagicNumber", DataType.DesigniteImplementationSmellsDataType, "Magic Number")
    MissingDefault = DataName("MissingDefault", DataType.DesigniteImplementationSmellsDataType, "Missing default")

    GodClass = DataName("GodClass", DataType.DesigniteOrganicTypeSmellsDataType, "God Class")
    ClassDataShouldBePrivate = DataName("ClassDataShouldBePrivate", DataType.DesigniteOrganicTypeSmellsDataType, "Class Data Should Be Private")
    ComplexClass = DataName("ComplexClass", DataType.DesigniteOrganicTypeSmellsDataType, "Complex Class")
    LazyClass = DataName("LazyClass", DataType.DesigniteOrganicTypeSmellsDataType, "Lazy Class")
    RefusedBequest = DataName("RefusedBequest", DataType.DesigniteOrganicTypeSmellsDataType, "Refused Bequest")
    SpaghettiCode = DataName("SpaghettiCode", DataType.DesigniteOrganicTypeSmellsDataType, "Spaghetti Code")
    SpeculativeGenerality = DataName("SpeculativeGenerality", DataType.DesigniteOrganicTypeSmellsDataType, "Speculative Generality")
    DataClass = DataName("DataClass", DataType.DesigniteOrganicTypeSmellsDataType, "Data Class")
    BrainClass = DataName("BrainClass", DataType.DesigniteOrganicTypeSmellsDataType, "Brain Class")
    LargeClass = DataName("LargeClass", DataType.DesigniteOrganicTypeSmellsDataType, "Large Class")
    SwissArmyKnife = DataName("SwissArmyKnife", DataType.DesigniteOrganicTypeSmellsDataType, "Swiss Army Knife")
    AntiSingleton = DataName("AntiSingleton", DataType.DesigniteOrganicTypeSmellsDataType, "Anti Singleton")

    FeatureEnvy = DataName("FeatureEnvy", DataType.DesigniteOrganicMethodSmellsDataType, "Feature Envy")
    LongMethod_Organic = DataName("LongMethod_Organic", DataType.DesigniteOrganicMethodSmellsDataType, "Long Method")
    LongParameterList_Organic = DataName("LongParameterList_Organic", DataType.DesigniteOrganicMethodSmellsDataType, "Long Parameter List")
    MessageChain = DataName("MessageChain", DataType.DesigniteOrganicMethodSmellsDataType, "Message Chain")
    DispersedCoupling = DataName("DispersedCoupling", DataType.DesigniteOrganicMethodSmellsDataType, "Dispersed Coupling")
    IntensiveCoupling = DataName("IntensiveCoupling", DataType.DesigniteOrganicMethodSmellsDataType, "Intensive Coupling")
    ShotgunSurgery = DataName("ShotgunSurgery", DataType.DesigniteOrganicMethodSmellsDataType, "Shotgun Surgery")
    BrainMethod = DataName("BrainMethod", DataType.DesigniteOrganicMethodSmellsDataType, "Brain Method")

    NumberOfFields = DataName("NumberOfFields", DataType.DesigniteTypeMetricsDataType, "NOF")
    NumberOfPublicFields = DataName("NumberOfPublicFields", DataType.DesigniteTypeMetricsDataType, "NOPF")
    NumberOfMethods_Designite = DataName("NumberOfMethods_Designite", DataType.DesigniteTypeMetricsDataType, "NOM")
    NumberOfPublicMethods_Designite = DataName("NumberOfPublicMethods_Designite", DataType.DesigniteTypeMetricsDataType, "NOPM")
    LOCClass = DataName("LOCClass", DataType.DesigniteTypeMetricsDataType, "LOC")
    WMC_Designite = DataName("WMC_Designite", DataType.DesigniteTypeMetricsDataType, "WMC")
    NumberOfChildren = DataName("NumberOfChildren", DataType.DesigniteTypeMetricsDataType, "NC")
    DepthOfInheritance = DataName("DepthOfInheritance", DataType.DesigniteTypeMetricsDataType, "DIT")
    LCOM = DataName("LCOM", DataType.DesigniteTypeMetricsDataType, "LCOM")
    FANIN = DataName("FANIN", DataType.DesigniteTypeMetricsDataType, "FANIN")
    FANOUT = DataName("FANOUT", DataType.DesigniteTypeMetricsDataType, "FANOUT")

    LOCMethod = DataName("LOCMethod", DataType.DesigniteMethodMetricsDataType, "LOC")
    CyclomaticComplexity_Designite = DataName("CyclomaticComplexity_Designite", DataType.DesigniteMethodMetricsDataType, "CC")
    NumberOfParameters_Designite = DataName("NumberOfParameters_Designite", DataType.DesigniteMethodMetricsDataType, "PC")

    NCSSForThisFile = DataName("NCSSForThisFile", DataType.CheckstyleDataType, "NCSS_for_this_file")
    NestedIfElseDepth = DataName("NestedIfElseDepth", DataType.CheckstyleDataType, "Nested_if-else_depth")
    BooleanExpressionComplexity = DataName("BooleanExpressionComplexity", DataType.CheckstyleDataType, "Boolean_expression_complexity")
    CyclomaticComplexity = DataName("CyclomaticComplexity", DataType.CheckstyleDataType, "Cyclomatic_Complexity")
    NCSSForThisMethod = DataName("NCSSForThisMethod", DataType.CheckstyleDataType, "NCSS_for_this_method")
    NPathComplexity = DataName("NPathComplexity", DataType.CheckstyleDataType, "NPath_Complexity")
    ThrowsCount = DataName("ThrowsCount", DataType.CheckstyleDataType, "Throws_count")
    NCSSForThisClass = DataName("NCSSForThisClass", DataType.CheckstyleDataType, "NCSS_for_this_class")
    NumberOfProtectedMethod = DataName("NumberOfProtectedMethod", DataType.CheckstyleDataType, "Number_of_protected_methods")
    NumberOfPackageMethod = DataName("NumberOfPackageMethod", DataType.CheckstyleDataType, "Number_of_package_methods")
    NumberOfPrivateMethod = DataName("NumberOfPrivateMethod", DataType.CheckstyleDataType, "Number_of_private_methods")
    ExecutableStatementCount = DataName("ExecutableStatementCount", DataType.CheckstyleDataType, "Executable_statement_count")
    MethodLength = DataName("MethodLength", DataType.CheckstyleDataType, "Method_length")
    FileLength = DataName("FileLength", DataType.CheckstyleDataType, "File_length")
    AnonymousInnerClassLength = DataName("AnonymousInnerClassLength", DataType.CheckstyleDataType, "Anonymous_inner_class_length")
    NumberOfMethods_Checkstyle = DataName("NumberOfMethods_Checkstyle", DataType.CheckstyleDataType, "Total_number_of_methods")
    NumberOfPublicMethods_Checkstyle = DataName("NumberOfPublicMethods_Checkstyle", DataType.CheckstyleDataType, "Number_of_public_methods")
    ClassFanOutComplexity = DataName("ClassFanOutComplexity", DataType.CheckstyleDataType, "Class_Fan-Out_Complexity")
    NestedTryDepth = DataName("NestedTryDepth", DataType.CheckstyleDataType, "Nested_try_depth")
    ClassDataAbstractionCoupling = DataName("ClassDataAbstractionCoupling", DataType.CheckstyleDataType, "Class_Data_Abstraction_Coupling")
    NestedForDepth = DataName("NestedForDepth", DataType.CheckstyleDataType, "Nested_for_depth")

    SourceMonitorComplexity = DataName("SourceMonitorComplexity", DataType.SourceMonitorDataType, "Complexity")
    SourceMonitorStatements = DataName("SourceMonitorStatements", DataType.SourceMonitorDataType, "Statements")
    SourceMonitorMaximumDepth = DataName("SourceMonitorMaximumDepth", DataType.SourceMonitorDataType, "Maximum Depth")
    SourceMonitorCalls = DataName("SourceMonitorCalls", DataType.SourceMonitorDataType, "Calls")

    SourceMonitorLines = DataName("SourceMonitorCalls", DataType.SourceMonitorFilesDataType, "Lines")
    SourceMonitorFileStatements = DataName("SourceMonitorFileStatements", DataType.SourceMonitorFilesDataType, "FileStatements")
    MethodCallStatements = DataName("MethodCallStatements", DataType.SourceMonitorFilesDataType, "Method Call Statements")
    PercentLinesWithComments = DataName("PercentLinesWithComments", DataType.SourceMonitorFilesDataType, "Percent Lines with Comments")
    ClassesandInterfaces = DataName("ClassesandInterfaces", DataType.SourceMonitorFilesDataType, "Classes and Interfaces")
    MethodsperClass = DataName("MethodsperClass", DataType.SourceMonitorFilesDataType, "Methods per Class")
    AverageStatementsperMethod = DataName("AverageStatementsperMethod", DataType.SourceMonitorFilesDataType, "Average Statements per Method")
    MaximumComplexity = DataName("MaximumComplexity", DataType.SourceMonitorFilesDataType, "Maximum Complexity*")
    MaximumBlockDepth = DataName("MaximumBlockDepth", DataType.SourceMonitorFilesDataType, "Maximum Block Depth")
    AverageBlockDepth = DataName("AverageBlockDepth", DataType.SourceMonitorFilesDataType, "Average Block Depth")
    AverageComplexity = DataName("AverageComplexity", DataType.SourceMonitorFilesDataType, "Average Complexity*")
    Statementsatblocklevel0 = DataName("Statementsatblocklevel0", DataType.SourceMonitorFilesDataType, "Statements at block level 0")
    Statementsatblocklevel1 = DataName("Statementsatblocklevel1", DataType.SourceMonitorFilesDataType, "Statements at block level 1")
    Statementsatblocklevel2 = DataName("Statementsatblocklevel2", DataType.SourceMonitorFilesDataType, "Statements at block level 2")
    Statementsatblocklevel3 = DataName("Statementsatblocklevel3", DataType.SourceMonitorFilesDataType, "Statements at block level 3")
    Statementsatblocklevel4 = DataName("Statementsatblocklevel4", DataType.SourceMonitorFilesDataType, "Statements at block level 4")
    Statementsatblocklevel5 = DataName("Statementsatblocklevel5", DataType.SourceMonitorFilesDataType, "Statements at block level 5")
    Statementsatblocklevel6 = DataName("Statementsatblocklevel6", DataType.SourceMonitorFilesDataType, "Statements at block level 6")
    Statementsatblocklevel7 = DataName("Statementsatblocklevel7", DataType.SourceMonitorFilesDataType, "Statements at block level 7")
    Statementsatblocklevel8 = DataName("Statementsatblocklevel8", DataType.SourceMonitorFilesDataType, "Statements at block level 8")
    Statementsatblocklevel9 = DataName("Statementsatblocklevel9", DataType.SourceMonitorFilesDataType, "Statements at block level 9")

    IsConstructor = DataName("IsConstructor", DataType.CKDataType, "constructor")
    CBO = DataName("CBO", DataType.CKDataType, "cbo")
    WMC_CK = DataName("WMC_CK", DataType.CKDataType, "wmc")
    RFC = DataName("RFC", DataType.CKDataType, "rfc")
    LOCMethod_CK = DataName("LOCMethod_CK", DataType.CKDataType, "loc")
    Returns = DataName("Returns", DataType.CKDataType, "returns")
    NumberOfVariables = DataName("NumberOfVariables", DataType.CKDataType, "variables")
    NumberOfParameters_CK = DataName("NumberOfParameters_CK", DataType.CKDataType, "parameters")
    NumberOfLoops = DataName("NumberOfLoops", DataType.CKDataType, "loopQty")
    NumberOfComparisons = DataName("NumberOfComparisons", DataType.CKDataType, "comparisonsQty")
    NumberOfTryCatch = DataName("NumberOfTryCatch", DataType.CKDataType, "tryCatchQty")
    NumberOfParenthesizedExps = DataName("NumberOfParenthesizedExps", DataType.CKDataType, "parenthesizedExpsQty")
    NumberOfStringLiterals = DataName("NumberOfStringLiterals", DataType.CKDataType, "stringLiteralsQty")
    NumberOfNumbers = DataName("NumberOfNumbers", DataType.CKDataType, "numbersQty")
    NumberOfAssignments = DataName("NumberOfAssignments", DataType.CKDataType, "assignmentsQty")
    NumberOfMathOperations = DataName("NumberOfMathOperations", DataType.CKDataType, "mathOperationsQty")
    MaxNumberOfNestedBlocks = DataName("MaxNumberOfNestedBlocks", DataType.CKDataType, "maxNestedBlocks")
    NumberOfAnonymousClasses = DataName("NumberOfAnonymousClasses", DataType.CKDataType, "anonymousClassesQty")
    NumberOfInnerClasses = DataName("NumberOfInnerClasses", DataType.CKDataType, "innerClassesQty")
    NumberOfLambdas = DataName("NumberOfLambdas", DataType.CKDataType, "lambdasQty")
    NumberOfUniqueWords = DataName("NumberOfUniqueWords", DataType.CKDataType, "uniqueWordsQty")
    NumberOfModifiers = DataName("NumberOfModifiers", DataType.CKDataType, "modifiers")
    NumberOfLogStatements = DataName("NumberOfLogStatements", DataType.CKDataType, "logStatementsQty")

    NumberOfAncestors = DataName("NumberOfAncestors", DataType.MoodDataType, "numberOfAncestors")
    NumberOfSubclasses = DataName("NumberOfSubclasses", DataType.MoodDataType, "numberOfSubclasses")
    NumberOfPrivateAttributes = DataName("NumberOfPrivateAttributes", DataType.MoodDataType, "numbeOfPrivateAttributes")
    NumberOfProtectedAttributes = DataName("NumberOfProtectedAttributes", DataType.MoodDataType, "numberOfProtectedAttributes")
    NumberOfPublicAttributes = DataName("NumberOfPublicAttributes", DataType.MoodDataType, "numberOfPublicAttributes")
    NumberOfAttributes = DataName("NumberOfAttributes", DataType.MoodDataType, "numberOfAttributes")
    NumberOfCoupledClasses = DataName("NumberOfCoupledClasses", DataType.MoodDataType, "numberOfCoupledClasses")
    Cohesion = DataName("Cohesion", DataType.MoodDataType, "cohesion")
    NumberOfMethods_Mood = DataName("NumberOfMethods_Mood", DataType.MoodDataType, "numberOfMethods")
    NumberPublicMethods = DataName("NumberPublicMethods", DataType.MoodDataType, "numberPublicMethods")
    NumberUserDefinedAttributes = DataName("NumberUserDefinedAttributes", DataType.MoodDataType, "numberUserDefinedAttributes")
    NumberOfInheritedMethods = DataName("NumberOfInheritedMethods", DataType.MoodDataType, "numberOfInheritedMethods")
    NumberOfPolymorphicMethods = DataName("NumberOfPolymorphicMethods", DataType.MoodDataType, "numberOfPolymorphicMethods")

    TotalNumberOfOperators = DataName("TotalNumberOfOperators", DataType.HalsteadDataType, "HalsteadTotalOperatorsCnt")
    NumberOfDistinctOperators = DataName("NumberOfDistinctOperators", DataType.HalsteadDataType, "HalsteadDistinctOperatorsCnt")
    TotalNumberOfOperands = DataName("TotalNumberOfOperands", DataType.HalsteadDataType, "HalsteadTotalOparandsCnt")
    NumberOfDistinctOperands = DataName("NumberOfDistinctOperands", DataType.HalsteadDataType, "HalsteadDistinctOperandsCnt")
    Length = DataName("Length", DataType.HalsteadDataType, "HalsteadLength")
    Vocabulary = DataName("Vocabulary", DataType.HalsteadDataType, "HalsteadVocabulary")
    Volume = DataName("Volume", DataType.HalsteadDataType, "HalsteadVolume")
    Difficulty = DataName("Difficulty", DataType.HalsteadDataType, "HalsteadDifficulty")
    Effort = DataName("Effort", DataType.HalsteadDataType, "HalsteadEffort")

    # jasome mood
    AHF = DataName("AHF", DataType.JasomeMoodDataType, "AHF", "Attribute Hiding Factor")
    AIF = DataName("AIF", DataType.JasomeMoodDataType, "AIF", "Attribute Inheritance Factor")
    MHF = DataName("MHF", DataType.JasomeMoodDataType, "MHF", "Method Hiding Factor")
    Aa = DataName("Aa", DataType.JasomeMoodDataType, "Aa", "Number of Attributes (All)")
    MIF = DataName("MIF", DataType.JasomeMoodDataType, "MIF", "Method Inheritance Factor")

    # jasome ck
    WMC = DataName("WMC", DataType.JasomeCKDataType, "WMC", "Weighted methods per Class")
    DIT = DataName("DIT", DataType.JasomeCKDataType, "DIT", "Depth of Inheritance Tree")
    NOCh = DataName("NOCh", DataType.JasomeCKDataType, "NOCh", "Number of Children")
    LCOMJASOME = DataName("LCOMJASOME", DataType.JasomeCKDataType, "LCOM*", "Lack of Cohesion Methods (H-S)")
    NMI = DataName("NMI", DataType.JasomeCKDataType, "NMI", "Number of Inherited Methods")
    NORM = DataName("NORM", DataType.JasomeCKDataType, "NORM", "Number of Overridden Methods")
    NPM = DataName("NPM", DataType.JasomeCKDataType, "NPM","Number of Public Methods")

    # jasome LORENZ AND KIDD
    SIX = DataName("SIX", DataType.JasomeLKDataType, "SIX", "Specialization Index")
    Ma = DataName("Ma", DataType.JasomeLKDataType, "Ma", "Number of Methods (All)")
    Md = DataName("Md", DataType.JasomeLKDataType, "Md", "Number of Methods Defined")
    Mi = DataName("Mi", DataType.JasomeLKDataType, "Mi", "Number of Methods Inherited and Not Overridden")
    Mit = DataName("Mit", DataType.JasomeLKDataType, "Mit", "Number of Methods Inherited (Total)")
    Mo = DataName("Mo", DataType.JasomeLKDataType, "Mo", "Number of Methods Overridden")
    NM = DataName("NM", DataType.JasomeLKDataType, "NM", "Number of Methods")
    NMA = DataName("NMA", DataType.JasomeLKDataType, "NMA", "Number of Methods Added to Inheritance")
    Ad = DataName("Ad", DataType.JasomeLKDataType, "Ad", "Number of Attributes Defined")
    NOPa = DataName("NOPa", DataType.JasomeLKDataType, "NOPa", "Number of Parents")
    Ai = DataName("Ai", DataType.JasomeLKDataType, "Ai", "Number of Attributes Inherited and Not Overridden")
    Ait = DataName("Ait", DataType.JasomeLKDataType, "Ait", "Number of Attributes Inherited (Total)")
    Ao = DataName("Ao", DataType.JasomeLKDataType, "Ao", "Number of Attributes Overridden")
    Av = DataName("Av", DataType.JasomeLKDataType, "Av", "Number of Public Attributes Defined")
    HMd = DataName("HMd", DataType.JasomeLKDataType, "HMd", "Number of Hidden Methods Defined")
    HMi = DataName("HMi", DataType.JasomeLKDataType, "HMi", "Number of Hidden Methods Inherited and Not Overridden")
    NF = DataName("NF", DataType.JasomeLKDataType, "NF", "Number of Attributes")
    NMIR = DataName("NMIR", DataType.JasomeLKDataType, "NMIR", "Number of Methods Inherited Ratio")
    PMi = DataName("PMi", DataType.JasomeLKDataType, "PMi", "Number of Public Methods Inherited and Not Overridden")
    PMR = DataName("PMR", DataType.JasomeLKDataType, "PMR", "Public Methods Ratio")

    # jasome Tegarden
    NOD = DataName("NOD", DataType.JasomeFilesDataType, "NOD", "Number of Descendants")
    NOA = DataName("NOA", DataType.JasomeFilesDataType, "NOA", "Number of Ancestors")

    # general jasome
    ClRCi = DataName("ClRCi", DataType.JasomeFilesDataType, "ClRCi", "Class Relative System Complexity")
    ClTCi = DataName("ClTCi", DataType.JasomeFilesDataType, "ClTCi", "Class Total System Complexity")
    NSM = DataName("NSM", DataType.JasomeFilesDataType, "NSM", "Number of Static Methods")
    NOL = DataName("NOL", DataType.JasomeFilesDataType, "NOL", "Number of Links")
    NPF = DataName("NPF", DataType.JasomeFilesDataType, "NPF", "Number of Public Attributes")
    NSF = DataName("NSF", DataType.JasomeFilesDataType, "NSF", "Number of Static Attributes")
    PMd = DataName("PMd", DataType.JasomeFilesDataType, "PMd", "Number of Public Methods Defined")
    RTLOC = DataName("RTLOC", DataType.JasomeFilesDataType, "RTLOC", "Raw Total Lines of Code")
    TLOC = DataName("TLOC", DataType.JasomeFilesDataType, "TLOC", "Total Lines of Code")

    Ci = DataName("Ci", DataType.JasomeMethodsDataType, "Ci", "System Complexity")
    Di = DataName("Di", DataType.JasomeMethodsDataType, "Di", "Data Complexity")
    Fin = DataName("Fin", DataType.JasomeMethodsDataType, "Fin", "Fan-in")
    Fout = DataName("Fout", DataType.JasomeMethodsDataType, "Fout", "Fan-out")
    IOVars = DataName("IOVars", DataType.JasomeMethodsDataType, "IOVars", "Input/Output Variables")
    MCLC = DataName("MCLC", DataType.JasomeMethodsDataType, "MCLC", "McClure's Complexity Metric")
    NBD = DataName("NBD", DataType.JasomeMethodsDataType, "NBD", "Nested Block Depth")
    NCOMP = DataName("NCOMP", DataType.JasomeMethodsDataType, "NCOMP", "Number of Comparisons")
    NOP = DataName("NOP", DataType.JasomeMethodsDataType, "NOP", "Number of Parameters")
    NVAR = DataName("NVAR", DataType.JasomeMethodsDataType, "NVAR", "Number of Control Variables")
    Si = DataName("Si", DataType.JasomeMethodsDataType, "Si", "Structural Complexity")
    VG = DataName("VG", DataType.JasomeMethodsDataType, "VG", "McCabe Cyclomatic Complexity")


    all_process_count = DataName("all_process_count", DataType.ProcessFilesDataType, "all_process_count")
    all_process_insertions_count = DataName("all_process_insertions_count", DataType.ProcessFilesDataType,
                                            "all_process_insertions_count")
    all_process_insertions_mean = DataName("all_process_insertions_mean", DataType.ProcessFilesDataType,
                                           "all_process_insertions_mean")
    all_process_insertions_std = DataName("all_process_insertions_std", DataType.ProcessFilesDataType,
                                          "all_process_insertions_std")
    all_process_insertions_min = DataName("all_process_insertions_min", DataType.ProcessFilesDataType,
                                          "all_process_insertions_min")
    all_process_insertions_max = DataName("all_process_insertions_max", DataType.ProcessFilesDataType,
                                          "all_process_insertions_max")
    all_process_deletions_count = DataName("all_process_deletions_count", DataType.ProcessFilesDataType,
                                           "all_process_deletions_count")
    all_process_deletions_mean = DataName("all_process_deletions_mean", DataType.ProcessFilesDataType,
                                          "all_process_deletions_mean")
    all_process_deletions_std = DataName("all_process_deletions_std", DataType.ProcessFilesDataType,
                                         "all_process_deletions_std")
    all_process_deletions_min = DataName("all_process_deletions_min", DataType.ProcessFilesDataType,
                                         "all_process_deletions_min")
    all_process_deletions_max = DataName("all_process_deletions_max", DataType.ProcessFilesDataType,
                                         "all_process_deletions_max")
    all_process_changes_count = DataName("all_process_changes_count", DataType.ProcessFilesDataType,
                                         "all_process_changes_count")
    all_process_changes_mean = DataName("all_process_changes_mean", DataType.ProcessFilesDataType,
                                        "all_process_changes_mean")
    all_process_changes_std = DataName("all_process_changes_std", DataType.ProcessFilesDataType,
                                       "all_process_changes_std")
    all_process_changes_min = DataName("all_process_changes_min", DataType.ProcessFilesDataType,
                                       "all_process_changes_min")
    all_process_changes_max = DataName("all_process_changes_max", DataType.ProcessFilesDataType,
                                       "all_process_changes_max")

    blame_merge_count = DataName("blame_merge_count", DataType.IssuesFilesDataType, "blame_merge_count")
    blame_merge_blame_getTotalOperatorsCnt_count = DataName("blame_merge_blame_getTotalOperatorsCnt_count",
                                                            DataType.IssuesFilesDataType,
                                                            "blame_merge_blame_getTotalOperatorsCnt_count")
    blame_merge_blame_getTotalOperatorsCnt_mean = DataName("blame_merge_blame_getTotalOperatorsCnt_mean",
                                                           DataType.IssuesFilesDataType,
                                                           "blame_merge_blame_getTotalOperatorsCnt_mean")
    blame_merge_blame_getTotalOperatorsCnt_std = DataName("blame_merge_blame_getTotalOperatorsCnt_std",
                                                          DataType.IssuesFilesDataType,
                                                          "blame_merge_blame_getTotalOperatorsCnt_std")
    blame_merge_blame_getTotalOperatorsCnt_min = DataName("blame_merge_blame_getTotalOperatorsCnt_min",
                                                          DataType.IssuesFilesDataType,
                                                          "blame_merge_blame_getTotalOperatorsCnt_min")
    blame_merge_blame_getTotalOperatorsCnt_max = DataName("blame_merge_blame_getTotalOperatorsCnt_max",
                                                          DataType.IssuesFilesDataType,
                                                          "blame_merge_blame_getTotalOperatorsCnt_max")
    blame_merge_blame_getDistinctOperatorsCnt_count = DataName("blame_merge_blame_getDistinctOperatorsCnt_count",
                                                               DataType.IssuesFilesDataType,
                                                               "blame_merge_blame_getDistinctOperatorsCnt_count")
    blame_merge_blame_getDistinctOperatorsCnt_mean = DataName("blame_merge_blame_getDistinctOperatorsCnt_mean",
                                                              DataType.IssuesFilesDataType,
                                                              "blame_merge_blame_getDistinctOperatorsCnt_mean")
    blame_merge_blame_getDistinctOperatorsCnt_std = DataName("blame_merge_blame_getDistinctOperatorsCnt_std",
                                                             DataType.IssuesFilesDataType,
                                                             "blame_merge_blame_getDistinctOperatorsCnt_std")
    blame_merge_blame_getDistinctOperatorsCnt_min = DataName("blame_merge_blame_getDistinctOperatorsCnt_min",
                                                             DataType.IssuesFilesDataType,
                                                             "blame_merge_blame_getDistinctOperatorsCnt_min")
    blame_merge_blame_getDistinctOperatorsCnt_max = DataName("blame_merge_blame_getDistinctOperatorsCnt_max",
                                                             DataType.IssuesFilesDataType,
                                                             "blame_merge_blame_getDistinctOperatorsCnt_max")
    blame_merge_blame_getTotalOparandsCnt_count = DataName("blame_merge_blame_getTotalOparandsCnt_count",
                                                           DataType.IssuesFilesDataType,
                                                           "blame_merge_blame_getTotalOparandsCnt_count")
    blame_merge_blame_getTotalOparandsCnt_mean = DataName("blame_merge_blame_getTotalOparandsCnt_mean",
                                                          DataType.IssuesFilesDataType,
                                                          "blame_merge_blame_getTotalOparandsCnt_mean")
    blame_merge_blame_getTotalOparandsCnt_std = DataName("blame_merge_blame_getTotalOparandsCnt_std",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_blame_getTotalOparandsCnt_std")
    blame_merge_blame_getTotalOparandsCnt_min = DataName("blame_merge_blame_getTotalOparandsCnt_min",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_blame_getTotalOparandsCnt_min")
    blame_merge_blame_getTotalOparandsCnt_max = DataName("blame_merge_blame_getTotalOparandsCnt_max",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_blame_getTotalOparandsCnt_max")
    blame_merge_blame_getDistinctOperandsCnt_count = DataName("blame_merge_blame_getDistinctOperandsCnt_count",
                                                              DataType.IssuesFilesDataType,
                                                              "blame_merge_blame_getDistinctOperandsCnt_count")
    blame_merge_blame_getDistinctOperandsCnt_mean = DataName("blame_merge_blame_getDistinctOperandsCnt_mean",
                                                             DataType.IssuesFilesDataType,
                                                             "blame_merge_blame_getDistinctOperandsCnt_mean")
    blame_merge_blame_getDistinctOperandsCnt_std = DataName("blame_merge_blame_getDistinctOperandsCnt_std",
                                                            DataType.IssuesFilesDataType,
                                                            "blame_merge_blame_getDistinctOperandsCnt_std")
    blame_merge_blame_getDistinctOperandsCnt_min = DataName("blame_merge_blame_getDistinctOperandsCnt_min",
                                                            DataType.IssuesFilesDataType,
                                                            "blame_merge_blame_getDistinctOperandsCnt_min")
    blame_merge_blame_getDistinctOperandsCnt_max = DataName("blame_merge_blame_getDistinctOperandsCnt_max",
                                                            DataType.IssuesFilesDataType,
                                                            "blame_merge_blame_getDistinctOperandsCnt_max")
    blame_merge_blame_getLength_count = DataName("blame_merge_blame_getLength_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_blame_getLength_count")
    blame_merge_blame_getLength_mean = DataName("blame_merge_blame_getLength_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_blame_getLength_mean")
    blame_merge_blame_getLength_std = DataName("blame_merge_blame_getLength_std", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getLength_std")
    blame_merge_blame_getLength_min = DataName("blame_merge_blame_getLength_min", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getLength_min")
    blame_merge_blame_getLength_max = DataName("blame_merge_blame_getLength_max", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getLength_max")
    blame_merge_blame_getVocabulary_count = DataName("blame_merge_blame_getVocabulary_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_blame_getVocabulary_count")
    blame_merge_blame_getVocabulary_mean = DataName("blame_merge_blame_getVocabulary_mean",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_blame_getVocabulary_mean")
    blame_merge_blame_getVocabulary_std = DataName("blame_merge_blame_getVocabulary_std", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getVocabulary_std")
    blame_merge_blame_getVocabulary_min = DataName("blame_merge_blame_getVocabulary_min", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getVocabulary_min")
    blame_merge_blame_getVocabulary_max = DataName("blame_merge_blame_getVocabulary_max", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getVocabulary_max")
    blame_merge_blame_getVolume_count = DataName("blame_merge_blame_getVolume_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_blame_getVolume_count")
    blame_merge_blame_getVolume_mean = DataName("blame_merge_blame_getVolume_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_blame_getVolume_mean")
    blame_merge_blame_getVolume_std = DataName("blame_merge_blame_getVolume_std", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getVolume_std")
    blame_merge_blame_getVolume_min = DataName("blame_merge_blame_getVolume_min", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getVolume_min")
    blame_merge_blame_getVolume_max = DataName("blame_merge_blame_getVolume_max", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getVolume_max")
    blame_merge_blame_getDifficulty_count = DataName("blame_merge_blame_getDifficulty_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_blame_getDifficulty_count")
    blame_merge_blame_getDifficulty_mean = DataName("blame_merge_blame_getDifficulty_mean",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_blame_getDifficulty_mean")
    blame_merge_blame_getDifficulty_std = DataName("blame_merge_blame_getDifficulty_std", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getDifficulty_std")
    blame_merge_blame_getDifficulty_min = DataName("blame_merge_blame_getDifficulty_min", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getDifficulty_min")
    blame_merge_blame_getDifficulty_max = DataName("blame_merge_blame_getDifficulty_max", DataType.IssuesFilesDataType,
                                                   "blame_merge_blame_getDifficulty_max")
    blame_merge_blame_getEffort_count = DataName("blame_merge_blame_getEffort_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_blame_getEffort_count")
    blame_merge_blame_getEffort_mean = DataName("blame_merge_blame_getEffort_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_blame_getEffort_mean")
    blame_merge_blame_getEffort_std = DataName("blame_merge_blame_getEffort_std", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getEffort_std")
    blame_merge_blame_getEffort_min = DataName("blame_merge_blame_getEffort_min", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getEffort_min")
    blame_merge_blame_getEffort_max = DataName("blame_merge_blame_getEffort_max", DataType.IssuesFilesDataType,
                                               "blame_merge_blame_getEffort_max")
    blame_merge_priorityBlocker_count = DataName("blame_merge_priorityBlocker_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_priorityBlocker_count")
    blame_merge_priorityBlocker_mean = DataName("blame_merge_priorityBlocker_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_priorityBlocker_mean")
    blame_merge_priorityBlocker_std = DataName("blame_merge_priorityBlocker_std", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityBlocker_std")
    blame_merge_priorityBlocker_min = DataName("blame_merge_priorityBlocker_min", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityBlocker_min")
    blame_merge_priorityBlocker_max = DataName("blame_merge_priorityBlocker_max", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityBlocker_max")
    blame_merge_priorityCritical_count = DataName("blame_merge_priorityCritical_count", DataType.IssuesFilesDataType,
                                                  "blame_merge_priorityCritical_count")
    blame_merge_priorityCritical_mean = DataName("blame_merge_priorityCritical_mean", DataType.IssuesFilesDataType,
                                                 "blame_merge_priorityCritical_mean")
    blame_merge_priorityCritical_std = DataName("blame_merge_priorityCritical_std", DataType.IssuesFilesDataType,
                                                "blame_merge_priorityCritical_std")
    blame_merge_priorityCritical_min = DataName("blame_merge_priorityCritical_min", DataType.IssuesFilesDataType,
                                                "blame_merge_priorityCritical_min")
    blame_merge_priorityCritical_max = DataName("blame_merge_priorityCritical_max", DataType.IssuesFilesDataType,
                                                "blame_merge_priorityCritical_max")
    blame_merge_priorityMajor_count = DataName("blame_merge_priorityMajor_count", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityMajor_count")
    blame_merge_priorityMajor_mean = DataName("blame_merge_priorityMajor_mean", DataType.IssuesFilesDataType,
                                              "blame_merge_priorityMajor_mean")
    blame_merge_priorityMajor_std = DataName("blame_merge_priorityMajor_std", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMajor_std")
    blame_merge_priorityMajor_min = DataName("blame_merge_priorityMajor_min", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMajor_min")
    blame_merge_priorityMajor_max = DataName("blame_merge_priorityMajor_max", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMajor_max")
    blame_merge_priorityMinor_count = DataName("blame_merge_priorityMinor_count", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityMinor_count")
    blame_merge_priorityMinor_mean = DataName("blame_merge_priorityMinor_mean", DataType.IssuesFilesDataType,
                                              "blame_merge_priorityMinor_mean")
    blame_merge_priorityMinor_std = DataName("blame_merge_priorityMinor_std", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMinor_std")
    blame_merge_priorityMinor_min = DataName("blame_merge_priorityMinor_min", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMinor_min")
    blame_merge_priorityMinor_max = DataName("blame_merge_priorityMinor_max", DataType.IssuesFilesDataType,
                                             "blame_merge_priorityMinor_max")
    blame_merge_priorityTrivial_count = DataName("blame_merge_priorityTrivial_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_priorityTrivial_count")
    blame_merge_priorityTrivial_mean = DataName("blame_merge_priorityTrivial_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_priorityTrivial_mean")
    blame_merge_priorityTrivial_std = DataName("blame_merge_priorityTrivial_std", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityTrivial_std")
    blame_merge_priorityTrivial_min = DataName("blame_merge_priorityTrivial_min", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityTrivial_min")
    blame_merge_priorityTrivial_max = DataName("blame_merge_priorityTrivial_max", DataType.IssuesFilesDataType,
                                               "blame_merge_priorityTrivial_max")
    blame_merge_resolutionCannotReproduce_count = DataName("blame_merge_resolutionCannotReproduce_count",
                                                           DataType.IssuesFilesDataType,
                                                           "blame_merge_resolutionCannotReproduce_count")
    blame_merge_resolutionCannotReproduce_mean = DataName("blame_merge_resolutionCannotReproduce_mean",
                                                          DataType.IssuesFilesDataType,
                                                          "blame_merge_resolutionCannotReproduce_mean")
    blame_merge_resolutionCannotReproduce_std = DataName("blame_merge_resolutionCannotReproduce_std",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_resolutionCannotReproduce_std")
    blame_merge_resolutionCannotReproduce_min = DataName("blame_merge_resolutionCannotReproduce_min",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_resolutionCannotReproduce_min")
    blame_merge_resolutionCannotReproduce_max = DataName("blame_merge_resolutionCannotReproduce_max",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_resolutionCannotReproduce_max")
    blame_merge_resolutionDuplicate_count = DataName("blame_merge_resolutionDuplicate_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_resolutionDuplicate_count")
    blame_merge_resolutionDuplicate_mean = DataName("blame_merge_resolutionDuplicate_mean",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_resolutionDuplicate_mean")
    blame_merge_resolutionDuplicate_std = DataName("blame_merge_resolutionDuplicate_std", DataType.IssuesFilesDataType,
                                                   "blame_merge_resolutionDuplicate_std")
    blame_merge_resolutionDuplicate_min = DataName("blame_merge_resolutionDuplicate_min", DataType.IssuesFilesDataType,
                                                   "blame_merge_resolutionDuplicate_min")
    blame_merge_resolutionDuplicate_max = DataName("blame_merge_resolutionDuplicate_max", DataType.IssuesFilesDataType,
                                                   "blame_merge_resolutionDuplicate_max")
    blame_merge_resolutionFixed_count = DataName("blame_merge_resolutionFixed_count", DataType.IssuesFilesDataType,
                                                 "blame_merge_resolutionFixed_count")
    blame_merge_resolutionFixed_mean = DataName("blame_merge_resolutionFixed_mean", DataType.IssuesFilesDataType,
                                                "blame_merge_resolutionFixed_mean")
    blame_merge_resolutionFixed_std = DataName("blame_merge_resolutionFixed_std", DataType.IssuesFilesDataType,
                                               "blame_merge_resolutionFixed_std")
    blame_merge_resolutionFixed_min = DataName("blame_merge_resolutionFixed_min", DataType.IssuesFilesDataType,
                                               "blame_merge_resolutionFixed_min")
    blame_merge_resolutionFixed_max = DataName("blame_merge_resolutionFixed_max", DataType.IssuesFilesDataType,
                                               "blame_merge_resolutionFixed_max")
    blame_merge_resolutionIncomplete_count = DataName("blame_merge_resolutionIncomplete_count",
                                                      DataType.IssuesFilesDataType,
                                                      "blame_merge_resolutionIncomplete_count")
    blame_merge_resolutionIncomplete_mean = DataName("blame_merge_resolutionIncomplete_mean",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_resolutionIncomplete_mean")
    blame_merge_resolutionIncomplete_std = DataName("blame_merge_resolutionIncomplete_std",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_resolutionIncomplete_std")
    blame_merge_resolutionIncomplete_min = DataName("blame_merge_resolutionIncomplete_min",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_resolutionIncomplete_min")
    blame_merge_resolutionIncomplete_max = DataName("blame_merge_resolutionIncomplete_max",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_resolutionIncomplete_max")
    blame_merge_resolutionNone_count = DataName("blame_merge_resolutionNone_count", DataType.IssuesFilesDataType,
                                                "blame_merge_resolutionNone_count")
    blame_merge_resolutionNone_mean = DataName("blame_merge_resolutionNone_mean", DataType.IssuesFilesDataType,
                                               "blame_merge_resolutionNone_mean")
    blame_merge_resolutionNone_std = DataName("blame_merge_resolutionNone_std", DataType.IssuesFilesDataType,
                                              "blame_merge_resolutionNone_std")
    blame_merge_resolutionNone_min = DataName("blame_merge_resolutionNone_min", DataType.IssuesFilesDataType,
                                              "blame_merge_resolutionNone_min")
    blame_merge_resolutionNone_max = DataName("blame_merge_resolutionNone_max", DataType.IssuesFilesDataType,
                                              "blame_merge_resolutionNone_max")
    blame_merge_resolutionNotAProblem_count = DataName("blame_merge_resolutionNotAProblem_count",
                                                       DataType.IssuesFilesDataType,
                                                       "blame_merge_resolutionNotAProblem_count")
    blame_merge_resolutionNotAProblem_mean = DataName("blame_merge_resolutionNotAProblem_mean",
                                                      DataType.IssuesFilesDataType,
                                                      "blame_merge_resolutionNotAProblem_mean")
    blame_merge_resolutionNotAProblem_std = DataName("blame_merge_resolutionNotAProblem_std",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_resolutionNotAProblem_std")
    blame_merge_resolutionNotAProblem_min = DataName("blame_merge_resolutionNotAProblem_min",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_resolutionNotAProblem_min")
    blame_merge_resolutionNotAProblem_max = DataName("blame_merge_resolutionNotAProblem_max",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_resolutionNotAProblem_max")
    blame_merge_resolutionPendingClosed_count = DataName("blame_merge_resolutionPendingClosed_count",
                                                         DataType.IssuesFilesDataType,
                                                         "blame_merge_resolutionPendingClosed_count")
    blame_merge_resolutionPendingClosed_mean = DataName("blame_merge_resolutionPendingClosed_mean",
                                                        DataType.IssuesFilesDataType,
                                                        "blame_merge_resolutionPendingClosed_mean")
    blame_merge_resolutionPendingClosed_std = DataName("blame_merge_resolutionPendingClosed_std",
                                                       DataType.IssuesFilesDataType,
                                                       "blame_merge_resolutionPendingClosed_std")
    blame_merge_resolutionPendingClosed_min = DataName("blame_merge_resolutionPendingClosed_min",
                                                       DataType.IssuesFilesDataType,
                                                       "blame_merge_resolutionPendingClosed_min")
    blame_merge_resolutionPendingClosed_max = DataName("blame_merge_resolutionPendingClosed_max",
                                                       DataType.IssuesFilesDataType,
                                                       "blame_merge_resolutionPendingClosed_max")
    blame_merge_resolutionWontFix_count = DataName("blame_merge_resolutionWontFix_count", DataType.IssuesFilesDataType,
                                                   "blame_merge_resolutionWontFix_count")
    blame_merge_resolutionWontFix_mean = DataName("blame_merge_resolutionWontFix_mean", DataType.IssuesFilesDataType,
                                                  "blame_merge_resolutionWontFix_mean")
    blame_merge_resolutionWontFix_std = DataName("blame_merge_resolutionWontFix_std", DataType.IssuesFilesDataType,
                                                 "blame_merge_resolutionWontFix_std")
    blame_merge_resolutionWontFix_min = DataName("blame_merge_resolutionWontFix_min", DataType.IssuesFilesDataType,
                                                 "blame_merge_resolutionWontFix_min")
    blame_merge_resolutionWontFix_max = DataName("blame_merge_resolutionWontFix_max", DataType.IssuesFilesDataType,
                                                 "blame_merge_resolutionWontFix_max")
    blame_merge_typeBug_count = DataName("blame_merge_typeBug_count", DataType.IssuesFilesDataType,
                                              "blame_merge_typeBug_count")
    blame_merge_typeBug_mean = DataName("blame_merge_typeBug_mean", DataType.IssuesFilesDataType,
                                             "blame_merge_typeBug_mean")
    blame_merge_typeBug_std = DataName("blame_merge_typeBug_std", DataType.IssuesFilesDataType,
                                            "blame_merge_typeBug_std")
    blame_merge_typeBug_min = DataName("blame_merge_typeBug_min", DataType.IssuesFilesDataType,
                                            "blame_merge_typeBug_min")
    blame_merge_typeBug_max = DataName("blame_merge_typeBug_max", DataType.IssuesFilesDataType,
                                            "blame_merge_typeBug_max")
    blame_merge_typeImprovement_count = DataName("blame_merge_typeImprovement_count",
                                                      DataType.IssuesFilesDataType,
                                                      "blame_merge_typeImprovement_count")
    blame_merge_typeImprovement_mean = DataName("blame_merge_typeImprovement_mean",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_typeImprovement_mean")
    blame_merge_typeImprovement_std = DataName("blame_merge_typeImprovement_std",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_typeImprovement_std")
    blame_merge_typeImprovement_min = DataName("blame_merge_typeImprovement_min",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_typeImprovement_min")
    blame_merge_typeImprovement_max = DataName("blame_merge_typeImprovement_max",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_typeImprovement_max")
    blame_merge_typeNewFeature_count = DataName("blame_merge_typeNewFeature_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blame_merge_typeNewFeature_count")
    blame_merge_typeNewFeature_mean = DataName("blame_merge_typeNewFeature_mean",
                                                    DataType.IssuesFilesDataType,
                                                    "blame_merge_typeNewFeature_mean")
    blame_merge_typeNewFeature_std = DataName("blame_merge_typeNewFeature_std", DataType.IssuesFilesDataType,
                                                   "blame_merge_typeNewFeature_std")
    blame_merge_typeNewFeature_min = DataName("blame_merge_typeNewFeature_min", DataType.IssuesFilesDataType,
                                                   "blame_merge_typeNewFeature_min")
    blame_merge_typeNewFeature_max = DataName("blame_merge_typeNewFeature_max", DataType.IssuesFilesDataType,
                                                   "blame_merge_typeNewFeature_max")
    blame_merge_typeQuestion_count = DataName("blame_merge_typeQuestion_count", DataType.IssuesFilesDataType,
                                                   "blame_merge_typeQuestion_count")
    blame_merge_typeQuestion_mean = DataName("blame_merge_typeQuestion_mean", DataType.IssuesFilesDataType,
                                                  "blame_merge_typeQuestion_mean")
    blame_merge_typeQuestion_std = DataName("blame_merge_typeQuestion_std", DataType.IssuesFilesDataType,
                                                 "blame_merge_typeQuestion_std")
    blame_merge_typeQuestion_min = DataName("blame_merge_typeQuestion_min", DataType.IssuesFilesDataType,
                                                 "blame_merge_typeQuestion_min")
    blame_merge_typeQuestion_max = DataName("blame_merge_typeQuestion_max", DataType.IssuesFilesDataType,
                                                 "blame_merge_typeQuestion_max")
    blame_merge_typeSubtask_count = DataName("blame_merge_typeSubtask_count", DataType.IssuesFilesDataType,
                                                  "blame_merge_typeSubtask_count")
    blame_merge_typeSubtask_mean = DataName("blame_merge_typeSubtask_mean", DataType.IssuesFilesDataType,
                                                 "blame_merge_typeSubtask_mean")
    blame_merge_typeSubtask_std = DataName("blame_merge_typeSubtask_std", DataType.IssuesFilesDataType,
                                                "blame_merge_typeSubtask_std")
    blame_merge_typeSubtask_min = DataName("blame_merge_typeSubtask_min", DataType.IssuesFilesDataType,
                                                "blame_merge_typeSubtask_min")
    blame_merge_typeSubtask_max = DataName("blame_merge_typeSubtask_max", DataType.IssuesFilesDataType,
                                                "blame_merge_typeSubtask_max")
    blame_merge_typeTask_count = DataName("blame_merge_typeTask_count", DataType.IssuesFilesDataType,
                                               "blame_merge_typeTask_count")
    blame_merge_typeTask_mean = DataName("blame_merge_typeTask_mean", DataType.IssuesFilesDataType,
                                              "blame_merge_typeTask_mean")
    blame_merge_typeTask_std = DataName("blame_merge_typeTask_std", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTask_std")
    blame_merge_typeTask_min = DataName("blame_merge_typeTask_min", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTask_min")
    blame_merge_typeTask_max = DataName("blame_merge_typeTask_max", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTask_max")
    blame_merge_typeTest_count = DataName("blame_merge_typeTest_count", DataType.IssuesFilesDataType,
                                               "blame_merge_typeTest_count")
    blame_merge_typeTest_mean = DataName("blame_merge_typeTest_mean", DataType.IssuesFilesDataType,
                                              "blame_merge_typeTest_mean")
    blame_merge_typeTest_std = DataName("blame_merge_typeTest_std", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTest_std")
    blame_merge_typeTest_min = DataName("blame_merge_typeTest_min", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTest_min")
    blame_merge_typeTest_max = DataName("blame_merge_typeTest_max", DataType.IssuesFilesDataType,
                                             "blame_merge_typeTest_max")
    blame_merge_typeWish_count = DataName("blame_merge_typeWish_count", DataType.IssuesFilesDataType,
                                               "blame_merge_typeWish_count")
    blame_merge_typeWish_mean = DataName("blame_merge_typeWish_mean", DataType.IssuesFilesDataType,
                                              "blame_merge_typeWish_mean")
    blame_merge_typeWish_std = DataName("blame_merge_typeWish_std", DataType.IssuesFilesDataType,
                                             "blame_merge_typeWish_std")
    blame_merge_typeWish_min = DataName("blame_merge_typeWish_min", DataType.IssuesFilesDataType,
                                             "blame_merge_typeWish_min")
    blame_merge_typeWish_max = DataName("blame_merge_typeWish_max", DataType.IssuesFilesDataType,
                                             "blame_merge_typeWish_max")
    fixes_count = DataName("fixes_count", DataType.IssuesFilesDataType, "fixes_count")
    fixes_insertions_count = DataName("fixes_insertions_count", DataType.IssuesFilesDataType, "fixes_insertions_count")
    fixes_insertions_mean = DataName("fixes_insertions_mean", DataType.IssuesFilesDataType, "fixes_insertions_mean")
    fixes_insertions_std = DataName("fixes_insertions_std", DataType.IssuesFilesDataType, "fixes_insertions_std")
    fixes_insertions_min = DataName("fixes_insertions_min", DataType.IssuesFilesDataType, "fixes_insertions_min")
    fixes_insertions_max = DataName("fixes_insertions_max", DataType.IssuesFilesDataType, "fixes_insertions_max")
    fixes_deletions_count = DataName("fixes_deletions_count", DataType.IssuesFilesDataType, "fixes_deletions_count")
    fixes_deletions_mean = DataName("fixes_deletions_mean", DataType.IssuesFilesDataType, "fixes_deletions_mean")
    fixes_deletions_std = DataName("fixes_deletions_std", DataType.IssuesFilesDataType, "fixes_deletions_std")
    fixes_deletions_min = DataName("fixes_deletions_min", DataType.IssuesFilesDataType, "fixes_deletions_min")
    fixes_deletions_max = DataName("fixes_deletions_max", DataType.IssuesFilesDataType, "fixes_deletions_max")
    fixes_changes_count = DataName("fixes_changes_count", DataType.IssuesFilesDataType, "fixes_changes_count")
    fixes_changes_mean = DataName("fixes_changes_mean", DataType.IssuesFilesDataType, "fixes_changes_mean")
    fixes_changes_std = DataName("fixes_changes_std", DataType.IssuesFilesDataType, "fixes_changes_std")
    fixes_changes_min = DataName("fixes_changes_min", DataType.IssuesFilesDataType, "fixes_changes_min")
    fixes_changes_max = DataName("fixes_changes_max", DataType.IssuesFilesDataType, "fixes_changes_max")
    non_fixes_count = DataName("non_fixes_count", DataType.IssuesFilesDataType, "non_fixes_count")
    non_fixes_insertions_count = DataName("non_fixes_insertions_count", DataType.IssuesFilesDataType,
                                          "non_fixes_insertions_count")
    non_fixes_insertions_mean = DataName("non_fixes_insertions_mean", DataType.IssuesFilesDataType,
                                         "non_fixes_insertions_mean")
    non_fixes_insertions_std = DataName("non_fixes_insertions_std", DataType.IssuesFilesDataType,
                                        "non_fixes_insertions_std")
    non_fixes_insertions_min = DataName("non_fixes_insertions_min", DataType.IssuesFilesDataType,
                                        "non_fixes_insertions_min")
    non_fixes_insertions_max = DataName("non_fixes_insertions_max", DataType.IssuesFilesDataType,
                                        "non_fixes_insertions_max")
    non_fixes_deletions_count = DataName("non_fixes_deletions_count", DataType.IssuesFilesDataType,
                                         "non_fixes_deletions_count")
    non_fixes_deletions_mean = DataName("non_fixes_deletions_mean", DataType.IssuesFilesDataType,
                                        "non_fixes_deletions_mean")
    non_fixes_deletions_std = DataName("non_fixes_deletions_std", DataType.IssuesFilesDataType,
                                       "non_fixes_deletions_std")
    non_fixes_deletions_min = DataName("non_fixes_deletions_min", DataType.IssuesFilesDataType,
                                       "non_fixes_deletions_min")
    non_fixes_deletions_max = DataName("non_fixes_deletions_max", DataType.IssuesFilesDataType,
                                       "non_fixes_deletions_max")
    non_fixes_changes_count = DataName("non_fixes_changes_count", DataType.IssuesFilesDataType,
                                       "non_fixes_changes_count")
    non_fixes_changes_mean = DataName("non_fixes_changes_mean", DataType.IssuesFilesDataType, "non_fixes_changes_mean")
    non_fixes_changes_std = DataName("non_fixes_changes_std", DataType.IssuesFilesDataType, "non_fixes_changes_std")
    non_fixes_changes_min = DataName("non_fixes_changes_min", DataType.IssuesFilesDataType, "non_fixes_changes_min")
    non_fixes_changes_max = DataName("non_fixes_changes_max", DataType.IssuesFilesDataType, "non_fixes_changes_max")
    issues_count = DataName("issues_count", DataType.IssuesFilesDataType, "issues_count")
    issues_insertions_count = DataName("issues_insertions_count", DataType.IssuesFilesDataType,
                                       "issues_insertions_count")
    issues_insertions_mean = DataName("issues_insertions_mean", DataType.IssuesFilesDataType, "issues_insertions_mean")
    issues_insertions_std = DataName("issues_insertions_std", DataType.IssuesFilesDataType, "issues_insertions_std")
    issues_insertions_min = DataName("issues_insertions_min", DataType.IssuesFilesDataType, "issues_insertions_min")
    issues_insertions_max = DataName("issues_insertions_max", DataType.IssuesFilesDataType, "issues_insertions_max")
    issues_deletions_count = DataName("issues_deletions_count", DataType.IssuesFilesDataType, "issues_deletions_count")
    issues_deletions_mean = DataName("issues_deletions_mean", DataType.IssuesFilesDataType, "issues_deletions_mean")
    issues_deletions_std = DataName("issues_deletions_std", DataType.IssuesFilesDataType, "issues_deletions_std")
    issues_deletions_min = DataName("issues_deletions_min", DataType.IssuesFilesDataType, "issues_deletions_min")
    issues_deletions_max = DataName("issues_deletions_max", DataType.IssuesFilesDataType, "issues_deletions_max")
    issues_changes_count = DataName("issues_changes_count", DataType.IssuesFilesDataType, "issues_changes_count")
    issues_changes_mean = DataName("issues_changes_mean", DataType.IssuesFilesDataType, "issues_changes_mean")
    issues_changes_std = DataName("issues_changes_std", DataType.IssuesFilesDataType, "issues_changes_std")
    issues_changes_min = DataName("issues_changes_min", DataType.IssuesFilesDataType, "issues_changes_min")
    issues_changes_max = DataName("issues_changes_max", DataType.IssuesFilesDataType, "issues_changes_max")
    issues_priorityBlocker_count = DataName("issues_priorityBlocker_count", DataType.IssuesFilesDataType,
                                            "issues_priorityBlocker_count")
    issues_priorityBlocker_mean = DataName("issues_priorityBlocker_mean", DataType.IssuesFilesDataType,
                                           "issues_priorityBlocker_mean")
    issues_priorityBlocker_std = DataName("issues_priorityBlocker_std", DataType.IssuesFilesDataType,
                                          "issues_priorityBlocker_std")
    issues_priorityBlocker_min = DataName("issues_priorityBlocker_min", DataType.IssuesFilesDataType,
                                          "issues_priorityBlocker_min")
    issues_priorityBlocker_max = DataName("issues_priorityBlocker_max", DataType.IssuesFilesDataType,
                                          "issues_priorityBlocker_max")
    issues_priorityCritical_count = DataName("issues_priorityCritical_count", DataType.IssuesFilesDataType,
                                             "issues_priorityCritical_count")
    issues_priorityCritical_mean = DataName("issues_priorityCritical_mean", DataType.IssuesFilesDataType,
                                            "issues_priorityCritical_mean")
    issues_priorityCritical_std = DataName("issues_priorityCritical_std", DataType.IssuesFilesDataType,
                                           "issues_priorityCritical_std")
    issues_priorityCritical_min = DataName("issues_priorityCritical_min", DataType.IssuesFilesDataType,
                                           "issues_priorityCritical_min")
    issues_priorityCritical_max = DataName("issues_priorityCritical_max", DataType.IssuesFilesDataType,
                                           "issues_priorityCritical_max")
    issues_priorityMajor_count = DataName("issues_priorityMajor_count", DataType.IssuesFilesDataType,
                                          "issues_priorityMajor_count")
    issues_priorityMajor_mean = DataName("issues_priorityMajor_mean", DataType.IssuesFilesDataType,
                                         "issues_priorityMajor_mean")
    issues_priorityMajor_std = DataName("issues_priorityMajor_std", DataType.IssuesFilesDataType,
                                        "issues_priorityMajor_std")
    issues_priorityMajor_min = DataName("issues_priorityMajor_min", DataType.IssuesFilesDataType,
                                        "issues_priorityMajor_min")
    issues_priorityMajor_max = DataName("issues_priorityMajor_max", DataType.IssuesFilesDataType,
                                        "issues_priorityMajor_max")
    issues_priorityMinor_count = DataName("issues_priorityMinor_count", DataType.IssuesFilesDataType,
                                          "issues_priorityMinor_count")
    issues_priorityMinor_mean = DataName("issues_priorityMinor_mean", DataType.IssuesFilesDataType,
                                         "issues_priorityMinor_mean")
    issues_priorityMinor_std = DataName("issues_priorityMinor_std", DataType.IssuesFilesDataType,
                                        "issues_priorityMinor_std")
    issues_priorityMinor_min = DataName("issues_priorityMinor_min", DataType.IssuesFilesDataType,
                                        "issues_priorityMinor_min")
    issues_priorityMinor_max = DataName("issues_priorityMinor_max", DataType.IssuesFilesDataType,
                                        "issues_priorityMinor_max")
    issues_priorityTrivial_count = DataName("issues_priorityTrivial_count", DataType.IssuesFilesDataType,
                                            "issues_priorityTrivial_count")
    issues_priorityTrivial_mean = DataName("issues_priorityTrivial_mean", DataType.IssuesFilesDataType,
                                           "issues_priorityTrivial_mean")
    issues_priorityTrivial_std = DataName("issues_priorityTrivial_std", DataType.IssuesFilesDataType,
                                          "issues_priorityTrivial_std")
    issues_priorityTrivial_min = DataName("issues_priorityTrivial_min", DataType.IssuesFilesDataType,
                                          "issues_priorityTrivial_min")
    issues_priorityTrivial_max = DataName("issues_priorityTrivial_max", DataType.IssuesFilesDataType,
                                          "issues_priorityTrivial_max")
    issues_resolutionCannotReproduce_count = DataName("issues_resolutionCannotReproduce_count",
                                                      DataType.IssuesFilesDataType,
                                                      "issues_resolutionCannotReproduce_count")
    issues_resolutionCannotReproduce_mean = DataName("issues_resolutionCannotReproduce_mean",
                                                     DataType.IssuesFilesDataType,
                                                     "issues_resolutionCannotReproduce_mean")
    issues_resolutionCannotReproduce_std = DataName("issues_resolutionCannotReproduce_std",
                                                    DataType.IssuesFilesDataType,
                                                    "issues_resolutionCannotReproduce_std")
    issues_resolutionCannotReproduce_min = DataName("issues_resolutionCannotReproduce_min",
                                                    DataType.IssuesFilesDataType,
                                                    "issues_resolutionCannotReproduce_min")
    issues_resolutionCannotReproduce_max = DataName("issues_resolutionCannotReproduce_max",
                                                    DataType.IssuesFilesDataType,
                                                    "issues_resolutionCannotReproduce_max")
    issues_resolutionDuplicate_count = DataName("issues_resolutionDuplicate_count", DataType.IssuesFilesDataType,
                                                "issues_resolutionDuplicate_count")
    issues_resolutionDuplicate_mean = DataName("issues_resolutionDuplicate_mean", DataType.IssuesFilesDataType,
                                               "issues_resolutionDuplicate_mean")
    issues_resolutionDuplicate_std = DataName("issues_resolutionDuplicate_std", DataType.IssuesFilesDataType,
                                              "issues_resolutionDuplicate_std")
    issues_resolutionDuplicate_min = DataName("issues_resolutionDuplicate_min", DataType.IssuesFilesDataType,
                                              "issues_resolutionDuplicate_min")
    issues_resolutionDuplicate_max = DataName("issues_resolutionDuplicate_max", DataType.IssuesFilesDataType,
                                              "issues_resolutionDuplicate_max")
    issues_resolutionFixed_count = DataName("issues_resolutionFixed_count", DataType.IssuesFilesDataType,
                                            "issues_resolutionFixed_count")
    issues_resolutionFixed_mean = DataName("issues_resolutionFixed_mean", DataType.IssuesFilesDataType,
                                           "issues_resolutionFixed_mean")
    issues_resolutionFixed_std = DataName("issues_resolutionFixed_std", DataType.IssuesFilesDataType,
                                          "issues_resolutionFixed_std")
    issues_resolutionFixed_min = DataName("issues_resolutionFixed_min", DataType.IssuesFilesDataType,
                                          "issues_resolutionFixed_min")
    issues_resolutionFixed_max = DataName("issues_resolutionFixed_max", DataType.IssuesFilesDataType,
                                          "issues_resolutionFixed_max")
    issues_resolutionIncomplete_count = DataName("issues_resolutionIncomplete_count", DataType.IssuesFilesDataType,
                                                 "issues_resolutionIncomplete_count")
    issues_resolutionIncomplete_mean = DataName("issues_resolutionIncomplete_mean", DataType.IssuesFilesDataType,
                                                "issues_resolutionIncomplete_mean")
    issues_resolutionIncomplete_std = DataName("issues_resolutionIncomplete_std", DataType.IssuesFilesDataType,
                                               "issues_resolutionIncomplete_std")
    issues_resolutionIncomplete_min = DataName("issues_resolutionIncomplete_min", DataType.IssuesFilesDataType,
                                               "issues_resolutionIncomplete_min")
    issues_resolutionIncomplete_max = DataName("issues_resolutionIncomplete_max", DataType.IssuesFilesDataType,
                                               "issues_resolutionIncomplete_max")
    issues_resolutionNone_count = DataName("issues_resolutionNone_count", DataType.IssuesFilesDataType,
                                           "issues_resolutionNone_count")
    issues_resolutionNone_mean = DataName("issues_resolutionNone_mean", DataType.IssuesFilesDataType,
                                          "issues_resolutionNone_mean")
    issues_resolutionNone_std = DataName("issues_resolutionNone_std", DataType.IssuesFilesDataType,
                                         "issues_resolutionNone_std")
    issues_resolutionNone_min = DataName("issues_resolutionNone_min", DataType.IssuesFilesDataType,
                                         "issues_resolutionNone_min")
    issues_resolutionNone_max = DataName("issues_resolutionNone_max", DataType.IssuesFilesDataType,
                                         "issues_resolutionNone_max")
    issues_resolutionNotAProblem_count = DataName("issues_resolutionNotAProblem_count", DataType.IssuesFilesDataType,
                                                  "issues_resolutionNotAProblem_count")
    issues_resolutionNotAProblem_mean = DataName("issues_resolutionNotAProblem_mean", DataType.IssuesFilesDataType,
                                                 "issues_resolutionNotAProblem_mean")
    issues_resolutionNotAProblem_std = DataName("issues_resolutionNotAProblem_std", DataType.IssuesFilesDataType,
                                                "issues_resolutionNotAProblem_std")
    issues_resolutionNotAProblem_min = DataName("issues_resolutionNotAProblem_min", DataType.IssuesFilesDataType,
                                                "issues_resolutionNotAProblem_min")
    issues_resolutionNotAProblem_max = DataName("issues_resolutionNotAProblem_max", DataType.IssuesFilesDataType,
                                                "issues_resolutionNotAProblem_max")
    issues_resolutionPendingClosed_count = DataName("issues_resolutionPendingClosed_count",
                                                    DataType.IssuesFilesDataType,
                                                    "issues_resolutionPendingClosed_count")
    issues_resolutionPendingClosed_mean = DataName("issues_resolutionPendingClosed_mean", DataType.IssuesFilesDataType,
                                                   "issues_resolutionPendingClosed_mean")
    issues_resolutionPendingClosed_std = DataName("issues_resolutionPendingClosed_std", DataType.IssuesFilesDataType,
                                                  "issues_resolutionPendingClosed_std")
    issues_resolutionPendingClosed_min = DataName("issues_resolutionPendingClosed_min", DataType.IssuesFilesDataType,
                                                  "issues_resolutionPendingClosed_min")
    issues_resolutionPendingClosed_max = DataName("issues_resolutionPendingClosed_max", DataType.IssuesFilesDataType,
                                                  "issues_resolutionPendingClosed_max")
    issues_resolutionWontFix_count = DataName("issues_resolutionWontFix_count", DataType.IssuesFilesDataType,
                                              "issues_resolutionWontFix_count")
    issues_resolutionWontFix_mean = DataName("issues_resolutionWontFix_mean", DataType.IssuesFilesDataType,
                                             "issues_resolutionWontFix_mean")
    issues_resolutionWontFix_std = DataName("issues_resolutionWontFix_std", DataType.IssuesFilesDataType,
                                            "issues_resolutionWontFix_std")
    issues_resolutionWontFix_min = DataName("issues_resolutionWontFix_min", DataType.IssuesFilesDataType,
                                            "issues_resolutionWontFix_min")
    issues_resolutionWontFix_max = DataName("issues_resolutionWontFix_max", DataType.IssuesFilesDataType,
                                            "issues_resolutionWontFix_max")
    issues_typeBug_count = DataName("issues_typeBug_count", DataType.IssuesFilesDataType,
                                         "issues_typeBug_count")
    issues_typeBug_mean = DataName("issues_typeBug_mean", DataType.IssuesFilesDataType,
                                        "issues_typeBug_mean")
    issues_typeBug_std = DataName("issues_typeBug_std", DataType.IssuesFilesDataType,
                                       "issues_typeBug_std")
    issues_typeBug_min = DataName("issues_typeBug_min", DataType.IssuesFilesDataType,
                                       "issues_typeBug_min")
    issues_typeBug_max = DataName("issues_typeBug_max", DataType.IssuesFilesDataType,
                                       "issues_typeBug_max")
    issues_typeImprovement_count = DataName("issues_typeImprovement_count", DataType.IssuesFilesDataType,
                                                 "issues_typeImprovement_count")
    issues_typeImprovement_mean = DataName("issues_typeImprovement_mean", DataType.IssuesFilesDataType,
                                                "issues_typeImprovement_mean")
    issues_typeImprovement_std = DataName("issues_typeImprovement_std", DataType.IssuesFilesDataType,
                                               "issues_typeImprovement_std")
    issues_typeImprovement_min = DataName("issues_typeImprovement_min", DataType.IssuesFilesDataType,
                                               "issues_typeImprovement_min")
    issues_typeImprovement_max = DataName("issues_typeImprovement_max", DataType.IssuesFilesDataType,
                                               "issues_typeImprovement_max")
    issues_typeNewFeature_count = DataName("issues_typeNewFeature_count", DataType.IssuesFilesDataType,
                                                "issues_typeNewFeature_count")
    issues_typeNewFeature_mean = DataName("issues_typeNewFeature_mean", DataType.IssuesFilesDataType,
                                               "issues_typeNewFeature_mean")
    issues_typeNewFeature_std = DataName("issues_typeNewFeature_std", DataType.IssuesFilesDataType,
                                              "issues_typeNewFeature_std")
    issues_typeNewFeature_min = DataName("issues_typeNewFeature_min", DataType.IssuesFilesDataType,
                                              "issues_typeNewFeature_min")
    issues_typeNewFeature_max = DataName("issues_typeNewFeature_max", DataType.IssuesFilesDataType,
                                              "issues_typeNewFeature_max")
    issues_typeQuestion_count = DataName("issues_typeQuestion_count", DataType.IssuesFilesDataType,
                                              "issues_typeQuestion_count")
    issues_typeQuestion_mean = DataName("issues_typeQuestion_mean", DataType.IssuesFilesDataType,
                                             "issues_typeQuestion_mean")
    issues_typeQuestion_std = DataName("issues_typeQuestion_std", DataType.IssuesFilesDataType,
                                            "issues_typeQuestion_std")
    issues_typeQuestion_min = DataName("issues_typeQuestion_min", DataType.IssuesFilesDataType,
                                            "issues_typeQuestion_min")
    issues_typeQuestion_max = DataName("issues_typeQuestion_max", DataType.IssuesFilesDataType,
                                            "issues_typeQuestion_max")
    issues_typeSubtask_count = DataName("issues_typeSubtask_count", DataType.IssuesFilesDataType,
                                             "issues_typeSubtask_count")
    issues_typeSubtask_mean = DataName("issues_typeSubtask_mean", DataType.IssuesFilesDataType,
                                            "issues_typeSubtask_mean")
    issues_typeSubtask_std = DataName("issues_typeSubtask_std", DataType.IssuesFilesDataType,
                                           "issues_typeSubtask_std")
    issues_typeSubtask_min = DataName("issues_typeSubtask_min", DataType.IssuesFilesDataType,
                                           "issues_typeSubtask_min")
    issues_typeSubtask_max = DataName("issues_typeSubtask_max", DataType.IssuesFilesDataType,
                                           "issues_typeSubtask_max")
    issues_typeTask_count = DataName("issues_typeTask_count", DataType.IssuesFilesDataType,
                                          "issues_typeTask_count")
    issues_typeTask_mean = DataName("issues_typeTask_mean", DataType.IssuesFilesDataType,
                                         "issues_typeTask_mean")
    issues_typeTask_std = DataName("issues_typeTask_std", DataType.IssuesFilesDataType,
                                        "issues_typeTask_std")
    issues_typeTask_min = DataName("issues_typeTask_min", DataType.IssuesFilesDataType,
                                        "issues_typeTask_min")
    issues_typeTask_max = DataName("issues_typeTask_max", DataType.IssuesFilesDataType,
                                        "issues_typeTask_max")
    issues_typeTest_count = DataName("issues_typeTest_count", DataType.IssuesFilesDataType,
                                          "issues_typeTest_count")
    issues_typeTest_mean = DataName("issues_typeTest_mean", DataType.IssuesFilesDataType,
                                         "issues_typeTest_mean")
    issues_typeTest_std = DataName("issues_typeTest_std", DataType.IssuesFilesDataType,
                                        "issues_typeTest_std")
    issues_typeTest_min = DataName("issues_typeTest_min", DataType.IssuesFilesDataType,
                                        "issues_typeTest_min")
    issues_typeTest_max = DataName("issues_typeTest_max", DataType.IssuesFilesDataType,
                                        "issues_typeTest_max")
    issues_typeWish_count = DataName("issues_typeWish_count", DataType.IssuesFilesDataType,
                                          "issues_typeWish_count")
    issues_typeWish_mean = DataName("issues_typeWish_mean", DataType.IssuesFilesDataType,
                                         "issues_typeWish_mean")
    issues_typeWish_std = DataName("issues_typeWish_std", DataType.IssuesFilesDataType,
                                        "issues_typeWish_std")
    issues_typeWish_min = DataName("issues_typeWish_min", DataType.IssuesFilesDataType,
                                        "issues_typeWish_min")
    issues_typeWish_max = DataName("issues_typeWish_max", DataType.IssuesFilesDataType,
                                        "issues_typeWish_max")
    blamemerge_blamegetTotalOperatorsCnt_count = DataName("blamemerge_blamegetTotalOperatorsCnt_count",
                                                          DataType.IssuesFilesDataType,
                                                          "blamemerge_blamegetTotalOperatorsCnt_count")
    blamemerge_blamegetTotalOperatorsCnt_mean = DataName("blamemerge_blamegetTotalOperatorsCnt_mean",
                                                         DataType.IssuesFilesDataType,
                                                         "blamemerge_blamegetTotalOperatorsCnt_mean")
    blamemerge_blamegetTotalOperatorsCnt_std = DataName("blamemerge_blamegetTotalOperatorsCnt_std",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_blamegetTotalOperatorsCnt_std")
    blamemerge_blamegetTotalOperatorsCnt_max = DataName("blamemerge_blamegetTotalOperatorsCnt_max",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_blamegetTotalOperatorsCnt_max")
    blamemerge_blamegetDistinctOperatorsCnt_count = DataName("blamemerge_blamegetDistinctOperatorsCnt_count",
                                                             DataType.IssuesFilesDataType,
                                                             "blamemerge_blamegetDistinctOperatorsCnt_count")
    blamemerge_blamegetDistinctOperatorsCnt_mean = DataName("blamemerge_blamegetDistinctOperatorsCnt_mean",
                                                            DataType.IssuesFilesDataType,
                                                            "blamemerge_blamegetDistinctOperatorsCnt_mean")
    blamemerge_blamegetDistinctOperatorsCnt_std = DataName("blamemerge_blamegetDistinctOperatorsCnt_std",
                                                           DataType.IssuesFilesDataType,
                                                           "blamemerge_blamegetDistinctOperatorsCnt_std")
    blamemerge_blamegetDistinctOperatorsCnt_max = DataName("blamemerge_blamegetDistinctOperatorsCnt_max",
                                                           DataType.IssuesFilesDataType,
                                                           "blamemerge_blamegetDistinctOperatorsCnt_max")
    blamemerge_blamegetTotalOparandsCnt_count = DataName("blamemerge_blamegetTotalOparandsCnt_count",
                                                         DataType.IssuesFilesDataType,
                                                         "blamemerge_blamegetTotalOparandsCnt_count")
    blamemerge_blamegetTotalOparandsCnt_mean = DataName("blamemerge_blamegetTotalOparandsCnt_mean",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_blamegetTotalOparandsCnt_mean")
    blamemerge_blamegetTotalOparandsCnt_std = DataName("blamemerge_blamegetTotalOparandsCnt_std",
                                                       DataType.IssuesFilesDataType,
                                                       "blamemerge_blamegetTotalOparandsCnt_std")
    blamemerge_blamegetTotalOparandsCnt_max = DataName("blamemerge_blamegetTotalOparandsCnt_max",
                                                       DataType.IssuesFilesDataType,
                                                       "blamemerge_blamegetTotalOparandsCnt_max")
    blamemerge_blamegetDistinctOperandsCnt_count = DataName("blamemerge_blamegetDistinctOperandsCnt_count",
                                                            DataType.IssuesFilesDataType,
                                                            "blamemerge_blamegetDistinctOperandsCnt_count")
    blamemerge_blamegetDistinctOperandsCnt_mean = DataName("blamemerge_blamegetDistinctOperandsCnt_mean",
                                                           DataType.IssuesFilesDataType,
                                                           "blamemerge_blamegetDistinctOperandsCnt_mean")
    blamemerge_blamegetDistinctOperandsCnt_std = DataName("blamemerge_blamegetDistinctOperandsCnt_std",
                                                          DataType.IssuesFilesDataType,
                                                          "blamemerge_blamegetDistinctOperandsCnt_std")
    blamemerge_blamegetDistinctOperandsCnt_max = DataName("blamemerge_blamegetDistinctOperandsCnt_max",
                                                          DataType.IssuesFilesDataType,
                                                          "blamemerge_blamegetDistinctOperandsCnt_max")
    blamemerge_blamegetLength_count = DataName("blamemerge_blamegetLength_count", DataType.IssuesFilesDataType,
                                               "blamemerge_blamegetLength_count")
    blamemerge_blamegetLength_mean = DataName("blamemerge_blamegetLength_mean", DataType.IssuesFilesDataType,
                                              "blamemerge_blamegetLength_mean")
    blamemerge_blamegetLength_std = DataName("blamemerge_blamegetLength_std", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetLength_std")
    blamemerge_blamegetLength_max = DataName("blamemerge_blamegetLength_max", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetLength_max")
    blamemerge_blamegetVocabulary_count = DataName("blamemerge_blamegetVocabulary_count", DataType.IssuesFilesDataType,
                                                   "blamemerge_blamegetVocabulary_count")
    blamemerge_blamegetVocabulary_mean = DataName("blamemerge_blamegetVocabulary_mean", DataType.IssuesFilesDataType,
                                                  "blamemerge_blamegetVocabulary_mean")
    blamemerge_blamegetVocabulary_std = DataName("blamemerge_blamegetVocabulary_std", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetVocabulary_std")
    blamemerge_blamegetVocabulary_max = DataName("blamemerge_blamegetVocabulary_max", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetVocabulary_max")
    blamemerge_blamegetVolume_count = DataName("blamemerge_blamegetVolume_count", DataType.IssuesFilesDataType,
                                               "blamemerge_blamegetVolume_count")
    blamemerge_blamegetVolume_mean = DataName("blamemerge_blamegetVolume_mean", DataType.IssuesFilesDataType,
                                              "blamemerge_blamegetVolume_mean")
    blamemerge_blamegetVolume_std = DataName("blamemerge_blamegetVolume_std", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetVolume_std")
    blamemerge_blamegetVolume_max = DataName("blamemerge_blamegetVolume_max", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetVolume_max")
    blamemerge_blamegetDifficulty_count = DataName("blamemerge_blamegetDifficulty_count", DataType.IssuesFilesDataType,
                                                   "blamemerge_blamegetDifficulty_count")
    blamemerge_blamegetDifficulty_mean = DataName("blamemerge_blamegetDifficulty_mean", DataType.IssuesFilesDataType,
                                                  "blamemerge_blamegetDifficulty_mean")
    blamemerge_blamegetDifficulty_std = DataName("blamemerge_blamegetDifficulty_std", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetDifficulty_std")
    blamemerge_blamegetDifficulty_max = DataName("blamemerge_blamegetDifficulty_max", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetDifficulty_max")
    blamemerge_blamegetEffort_count = DataName("blamemerge_blamegetEffort_count", DataType.IssuesFilesDataType,
                                               "blamemerge_blamegetEffort_count")
    blamemerge_blamegetEffort_mean = DataName("blamemerge_blamegetEffort_mean", DataType.IssuesFilesDataType,
                                              "blamemerge_blamegetEffort_mean")
    blamemerge_blamegetEffort_std = DataName("blamemerge_blamegetEffort_std", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetEffort_std")
    blamemerge_blamegetEffort_max = DataName("blamemerge_blamegetEffort_max", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetEffort_max")
    blamemerge_priorityBlocker_count = DataName("blamemerge_priorityBlocker_count", DataType.IssuesFilesDataType,
                                                "blamemerge_priorityBlocker_count")
    blamemerge_priorityCritical_count = DataName("blamemerge_priorityCritical_count", DataType.IssuesFilesDataType,
                                                 "blamemerge_priorityCritical_count")
    blamemerge_priorityMajor_count = DataName("blamemerge_priorityMajor_count", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityMajor_count")
    blamemerge_priorityMajor_mean = DataName("blamemerge_priorityMajor_mean", DataType.IssuesFilesDataType,
                                             "blamemerge_priorityMajor_mean")
    blamemerge_priorityMajor_min = DataName("blamemerge_priorityMajor_min", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMajor_min")
    blamemerge_priorityMajor_max = DataName("blamemerge_priorityMajor_max", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMajor_max")
    blamemerge_priorityMinor_count = DataName("blamemerge_priorityMinor_count", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityMinor_count")
    blamemerge_priorityTrivial_count = DataName("blamemerge_priorityTrivial_count", DataType.IssuesFilesDataType,
                                                "blamemerge_priorityTrivial_count")
    blamemerge_resolutionCannotReproduce_count = DataName("blamemerge_resolutionCannotReproduce_count",
                                                          DataType.IssuesFilesDataType,
                                                          "blamemerge_resolutionCannotReproduce_count")
    blamemerge_resolutionDuplicate_count = DataName("blamemerge_resolutionDuplicate_count",
                                                    DataType.IssuesFilesDataType,
                                                    "blamemerge_resolutionDuplicate_count")
    blamemerge_resolutionFixed_count = DataName("blamemerge_resolutionFixed_count", DataType.IssuesFilesDataType,
                                                "blamemerge_resolutionFixed_count")
    blamemerge_resolutionFixed_mean = DataName("blamemerge_resolutionFixed_mean", DataType.IssuesFilesDataType,
                                               "blamemerge_resolutionFixed_mean")
    blamemerge_resolutionFixed_min = DataName("blamemerge_resolutionFixed_min", DataType.IssuesFilesDataType,
                                              "blamemerge_resolutionFixed_min")
    blamemerge_resolutionFixed_max = DataName("blamemerge_resolutionFixed_max", DataType.IssuesFilesDataType,
                                              "blamemerge_resolutionFixed_max")
    blamemerge_resolutionIncomplete_count = DataName("blamemerge_resolutionIncomplete_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blamemerge_resolutionIncomplete_count")
    blamemerge_resolutionNone_count = DataName("blamemerge_resolutionNone_count", DataType.IssuesFilesDataType,
                                               "blamemerge_resolutionNone_count")
    blamemerge_resolutionNotAProblem_count = DataName("blamemerge_resolutionNotAProblem_count",
                                                      DataType.IssuesFilesDataType,
                                                      "blamemerge_resolutionNotAProblem_count")
    blamemerge_resolutionPendingClosed_count = DataName("blamemerge_resolutionPendingClosed_count",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_resolutionPendingClosed_count")
    blamemerge_resolutionWontFix_count = DataName("blamemerge_resolutionWontFix_count", DataType.IssuesFilesDataType,
                                                  "blamemerge_resolutionWontFix_count")
    blamemerge_typeBug_count = DataName("blamemerge_typeBug_count", DataType.IssuesFilesDataType,
                                             "blamemerge_typeBug_count")
    blamemerge_typeImprovement_count = DataName("blamemerge_typeImprovement_count",
                                                     DataType.IssuesFilesDataType,
                                                     "blamemerge_typeImprovement_count")
    blamemerge_typeNewFeature_count = DataName("blamemerge_typeNewFeature_count",
                                                    DataType.IssuesFilesDataType,
                                                    "blamemerge_typeNewFeature_count")
    blamemerge_typeNewFeature_mean = DataName("blamemerge_typeNewFeature_mean", DataType.IssuesFilesDataType,
                                                   "blamemerge_typeNewFeature_mean")
    blamemerge_typeNewFeature_min = DataName("blamemerge_typeNewFeature_min", DataType.IssuesFilesDataType,
                                                  "blamemerge_typeNewFeature_min")
    blamemerge_typeNewFeature_max = DataName("blamemerge_typeNewFeature_max", DataType.IssuesFilesDataType,
                                                  "blamemerge_typeNewFeature_max")
    blamemerge_typeQuestion_count = DataName("blamemerge_typeQuestion_count", DataType.IssuesFilesDataType,
                                                  "blamemerge_typeQuestion_count")
    blamemerge_typeSubtask_count = DataName("blamemerge_typeSubtask_count", DataType.IssuesFilesDataType,
                                                 "blamemerge_typeSubtask_count")
    blamemerge_typeTask_count = DataName("blamemerge_typeTask_count", DataType.IssuesFilesDataType,
                                              "blamemerge_typeTask_count")
    blamemerge_typeTest_count = DataName("blamemerge_typeTest_count", DataType.IssuesFilesDataType,
                                              "blamemerge_typeTest_count")
    blamemerge_typeWish_count = DataName("blamemerge_typeWish_count", DataType.IssuesFilesDataType,
                                              "blamemerge_typeWish_count")
    blamemerge_typeImprovement_mean = DataName("blamemerge_typeImprovement_mean",
                                                    DataType.IssuesFilesDataType,
                                                    "blamemerge_typeImprovement_mean")
    blamemerge_typeImprovement_std = DataName("blamemerge_typeImprovement_std", DataType.IssuesFilesDataType,
                                                   "blamemerge_typeImprovement_std")
    blamemerge_typeImprovement_max = DataName("blamemerge_typeImprovement_max", DataType.IssuesFilesDataType,
                                                   "blamemerge_typeImprovement_max")
    blamemerge_typeNewFeature_std = DataName("blamemerge_typeNewFeature_std", DataType.IssuesFilesDataType,
                                                  "blamemerge_typeNewFeature_std")
    blamemerge_typeSubtask_mean = DataName("blamemerge_typeSubtask_mean", DataType.IssuesFilesDataType,
                                                "blamemerge_typeSubtask_mean")
    blamemerge_typeSubtask_std = DataName("blamemerge_typeSubtask_std", DataType.IssuesFilesDataType,
                                               "blamemerge_typeSubtask_std")
    blamemerge_typeSubtask_max = DataName("blamemerge_typeSubtask_max", DataType.IssuesFilesDataType,
                                               "blamemerge_typeSubtask_max")
    blamemerge_blamegetTotalOperatorsCnt_min = DataName("blamemerge_blamegetTotalOperatorsCnt_min",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_blamegetTotalOperatorsCnt_min")
    blamemerge_blamegetDistinctOperatorsCnt_min = DataName("blamemerge_blamegetDistinctOperatorsCnt_min",
                                                           DataType.IssuesFilesDataType,
                                                           "blamemerge_blamegetDistinctOperatorsCnt_min")
    blamemerge_blamegetTotalOparandsCnt_min = DataName("blamemerge_blamegetTotalOparandsCnt_min",
                                                       DataType.IssuesFilesDataType,
                                                       "blamemerge_blamegetTotalOparandsCnt_min")
    blamemerge_blamegetDistinctOperandsCnt_min = DataName("blamemerge_blamegetDistinctOperandsCnt_min",
                                                          DataType.IssuesFilesDataType,
                                                          "blamemerge_blamegetDistinctOperandsCnt_min")
    blamemerge_blamegetLength_min = DataName("blamemerge_blamegetLength_min", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetLength_min")
    blamemerge_blamegetVocabulary_min = DataName("blamemerge_blamegetVocabulary_min", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetVocabulary_min")
    blamemerge_blamegetVolume_min = DataName("blamemerge_blamegetVolume_min", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetVolume_min")
    blamemerge_blamegetDifficulty_min = DataName("blamemerge_blamegetDifficulty_min", DataType.IssuesFilesDataType,
                                                 "blamemerge_blamegetDifficulty_min")
    blamemerge_blamegetEffort_min = DataName("blamemerge_blamegetEffort_min", DataType.IssuesFilesDataType,
                                             "blamemerge_blamegetEffort_min")
    blamemerge_typeBug_mean = DataName("blamemerge_typeBug_mean", DataType.IssuesFilesDataType,
                                            "blamemerge_typeBug_mean")
    blamemerge_typeBug_min = DataName("blamemerge_typeBug_min", DataType.IssuesFilesDataType,
                                           "blamemerge_typeBug_min")
    blamemerge_typeBug_max = DataName("blamemerge_typeBug_max", DataType.IssuesFilesDataType,
                                           "blamemerge_typeBug_max")
    blamemerge_priorityMinor_mean = DataName("blamemerge_priorityMinor_mean", DataType.IssuesFilesDataType,
                                             "blamemerge_priorityMinor_mean")
    blamemerge_priorityMinor_min = DataName("blamemerge_priorityMinor_min", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMinor_min")
    blamemerge_priorityMinor_max = DataName("blamemerge_priorityMinor_max", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMinor_max")
    blamemerge_typeImprovement_min = DataName("blamemerge_typeImprovement_min", DataType.IssuesFilesDataType,
                                                   "blamemerge_typeImprovement_min")
    blamemerge_typeBug_std = DataName("blamemerge_typeBug_std", DataType.IssuesFilesDataType,
                                           "blamemerge_typeBug_std")
    blamemerge_priorityMajor_std = DataName("blamemerge_priorityMajor_std", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMajor_std")
    blamemerge_priorityMinor_std = DataName("blamemerge_priorityMinor_std", DataType.IssuesFilesDataType,
                                            "blamemerge_priorityMinor_std")
    blamemerge_priorityBlocker_mean = DataName("blamemerge_priorityBlocker_mean", DataType.IssuesFilesDataType,
                                               "blamemerge_priorityBlocker_mean")
    blamemerge_priorityBlocker_std = DataName("blamemerge_priorityBlocker_std", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityBlocker_std")
    blamemerge_priorityBlocker_max = DataName("blamemerge_priorityBlocker_max", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityBlocker_max")
    blamemerge_priorityCritical_mean = DataName("blamemerge_priorityCritical_mean", DataType.IssuesFilesDataType,
                                                "blamemerge_priorityCritical_mean")
    blamemerge_priorityCritical_std = DataName("blamemerge_priorityCritical_std", DataType.IssuesFilesDataType,
                                               "blamemerge_priorityCritical_std")
    blamemerge_priorityCritical_max = DataName("blamemerge_priorityCritical_max", DataType.IssuesFilesDataType,
                                               "blamemerge_priorityCritical_max")
    blamemerge_typeTask_mean = DataName("blamemerge_typeTask_mean", DataType.IssuesFilesDataType,
                                             "blamemerge_typeTask_mean")
    blamemerge_typeTask_std = DataName("blamemerge_typeTask_std", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTask_std")
    blamemerge_typeTask_max = DataName("blamemerge_typeTask_max", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTask_max")
    blamemerge_resolutionFixed_std = DataName("blamemerge_resolutionFixed_std", DataType.IssuesFilesDataType,
                                              "blamemerge_resolutionFixed_std")
    blamemerge_resolutionNone_mean = DataName("blamemerge_resolutionNone_mean", DataType.IssuesFilesDataType,
                                              "blamemerge_resolutionNone_mean")
    blamemerge_resolutionNone_std = DataName("blamemerge_resolutionNone_std", DataType.IssuesFilesDataType,
                                             "blamemerge_resolutionNone_std")
    blamemerge_resolutionNone_max = DataName("blamemerge_resolutionNone_max", DataType.IssuesFilesDataType,
                                             "blamemerge_resolutionNone_max")
    blamemerge_typeSubtask_min = DataName("blamemerge_typeSubtask_min", DataType.IssuesFilesDataType,
                                               "blamemerge_typeSubtask_min")
    blamemerge_resolutionNone_min = DataName("blamemerge_resolutionNone_min", DataType.IssuesFilesDataType,
                                             "blamemerge_resolutionNone_min")
    blamemerge_resolutionWontFix_mean = DataName("blamemerge_resolutionWontFix_mean", DataType.IssuesFilesDataType,
                                                 "blamemerge_resolutionWontFix_mean")
    blamemerge_resolutionWontFix_std = DataName("blamemerge_resolutionWontFix_std", DataType.IssuesFilesDataType,
                                                "blamemerge_resolutionWontFix_std")
    blamemerge_resolutionWontFix_max = DataName("blamemerge_resolutionWontFix_max", DataType.IssuesFilesDataType,
                                                "blamemerge_resolutionWontFix_max")
    blamemerge_priorityTrivial_mean = DataName("blamemerge_priorityTrivial_mean", DataType.IssuesFilesDataType,
                                               "blamemerge_priorityTrivial_mean")
    blamemerge_priorityTrivial_std = DataName("blamemerge_priorityTrivial_std", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityTrivial_std")
    blamemerge_priorityTrivial_max = DataName("blamemerge_priorityTrivial_max", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityTrivial_max")
    blamemerge_typeTask_min = DataName("blamemerge_typeTask_min", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTask_min")
    blamemerge_resolutionCannotReproduce_mean = DataName("blamemerge_resolutionCannotReproduce_mean",
                                                         DataType.IssuesFilesDataType,
                                                         "blamemerge_resolutionCannotReproduce_mean")
    blamemerge_resolutionCannotReproduce_std = DataName("blamemerge_resolutionCannotReproduce_std",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_resolutionCannotReproduce_std")
    blamemerge_resolutionCannotReproduce_max = DataName("blamemerge_resolutionCannotReproduce_max",
                                                        DataType.IssuesFilesDataType,
                                                        "blamemerge_resolutionCannotReproduce_max")
    blamemerge_typeWish_mean = DataName("blamemerge_typeWish_mean", DataType.IssuesFilesDataType,
                                             "blamemerge_typeWish_mean")
    blamemerge_typeWish_std = DataName("blamemerge_typeWish_std", DataType.IssuesFilesDataType,
                                            "blamemerge_typeWish_std")
    blamemerge_typeWish_max = DataName("blamemerge_typeWish_max", DataType.IssuesFilesDataType,
                                            "blamemerge_typeWish_max")
    blamemerge_priorityBlocker_min = DataName("blamemerge_priorityBlocker_min", DataType.IssuesFilesDataType,
                                              "blamemerge_priorityBlocker_min")
    blamemerge_priorityCritical_min = DataName("blamemerge_priorityCritical_min", DataType.IssuesFilesDataType,
                                               "blamemerge_priorityCritical_min")
    blamemerge_typeTest_mean = DataName("blamemerge_typeTest_mean", DataType.IssuesFilesDataType,
                                             "blamemerge_typeTest_mean")
    blamemerge_typeTest_std = DataName("blamemerge_typeTest_std", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTest_std")
    blamemerge_typeTest_max = DataName("blamemerge_typeTest_max", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTest_max")
    blamemerge_typeTest_min = DataName("blamemerge_typeTest_min", DataType.IssuesFilesDataType,
                                            "blamemerge_typeTest_min")

    @staticmethod
    def get_data_names_by_type(data_types: List[DataType]):
        ans = []
        for d in DataNameEnum:
            if d.value.data_type in data_types:
                ans.append(d)
        return ans


if __name__ == "__main__":
    by_types = {}
    for d in DataNameEnum:
        by_types.setdefault(d.value.data_type.name, []).append(d.value.name)
    for d in by_types:
        print(d)
        for k in by_types[d]:
            print('\t-' + k)
    pass