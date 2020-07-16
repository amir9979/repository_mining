from enum import Enum, auto


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


class DataName:
    def __init__(self, name, data_type: DataType, column_name, description=""):
        self.name = name
        self.data_type = data_type
        self.data_type_value = data_type.value
        self.column_name = column_name
        self.description = description

    def as_data_dict(self):
        return {'data_value': self.name, 'data_type': self.data_type_value, 'data_column': self.column_name}

    def as_description_dict(self):
        return {"feature_name": self.name, "feature_group": self.data_type_value, "column_name": self.column_name, "description": self.description}


class DataNameEnum(Enum):
    # TODO create accessors for each enumeration
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

    # TODO SourceMonitorColumns - Need windows to do this
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

    TotalNumberOfOperators = DataName("TotalNumberOfOperators", DataType.HalsteadDataType, "getTotalOperatorsCnt")
    NumberOfDistinctOperators = DataName("NumberOfDistinctOperators", DataType.HalsteadDataType, "getDistinctOperatorsCnt")
    TotalNumberOfOperands = DataName("TotalNumberOfOperands", DataType.HalsteadDataType, "getTotalOparandsCnt")
    NumberOfDistinctOperands = DataName("NumberOfDistinctOperands", DataType.HalsteadDataType, "getDistinctOperandsCnt")
    Length = DataName("Length", DataType.HalsteadDataType, "getLength")
    Vocabulary = DataName("Vocabulary", DataType.HalsteadDataType, "getVocabulary")
    Volume = DataName("Volume", DataType.HalsteadDataType, "getVolume")
    Difficulty = DataName("Difficulty", DataType.HalsteadDataType, "getDifficulty")
    Effort = DataName("Effort", DataType.HalsteadDataType, "getEffort")
