# repository_mining

## TODO
- [ ] SpotBugs

## Tools
| Tool | Description | Implemented? |
| ---- | ----------- | ------------ |
| [Spotbugs](https://spotbugs.github.io/) | SpotBugs is a program which uses static analysis to look for bugs in Java code. | No |
| [DesigniteJava](https://github.com/tushartushar/DesigniteJava) | DesigniteJava is a code quality assessment tool for code written in Java. | Yes |
| [Checkstyle](https://github.com/checkstyle/checkstyle) | Checkstyle is a development tool to help programmers write Java code that adheres to a coding standard. | Yes |
| [CK](https://github.com/mauricioaniche/ck) | CK calculates class-level and metric-level code metrics in Java projects by means of static analysis (i.e. no need for compiled code). | Yes |
| [AwesomeStaticAnalysis](https://github.com/analysis-tools-dev/static-analysis) | This is a collection of static analysis tools and code quality checkers | No |
| [Coming](https://github.com/SpoonLabs/coming) | Coming is a tool for mining git repositories | No |
| [Organic](https://github.com/opus-research/organic) | This project is an Eclipse plugin that aims to collect code smells from Java projects using only command line tools. | Yes |
| [TSE2015TDIdentification](https://github.com/maldonado/tse2015_td_identification) | Npl tool to mine closed sequential patterns | No |
| [SourceMonitor](http://www.campwoodsw.com/sourcemonitor.html) | The freeware program SourceMonitor lets you see inside your software source code to find out how much code you have and to identify the relative complexity of your modules. | Yes |
| [ConcernReCS](https://sourceforge.net/p/concernrecs/home/Home/) | ConcernReCS is an Eclipse plug-in written to find Aspectization Code Smells, i.e., scenarios in source code that can lead to aspectization mistakes.) | No | 
| [Sonarqube](https://www.sonarqube.org/) | Thousands of automated Static Code Analysis rules. | No |
| [Halstead](https://github.com/dborowiec/commentedCodeDetector) | The tool detects commented code using heuristics based on usage of Halstead code metrics | Yes |
| [gorgeous_metrics](https://github.com/thainamariani/gorgeous_metrics) | MOOD Metrics | Yes |
| [JaSoMe](https://github.com/rodhilton/jasome) | Jasome (JAH-suhm, rhymes with awesome) is a source code analyzer that mines internal quality metrics from projects based on source code alone | Yes |
 
    
## Metrics
### Categories
#### Product Metrics
- CK
    - WMC - Weighted Method Count
    - DIT - Depth of Inheritance Tree
    - RFC - Response For Class
    - NOC - Number of Children
    - CBO - Coupling Between Objects
    - LCOM - Lack of Cohesion in Methods
    
- OO
    - FanIn - Number of other classes that reference the class
    - FanOut - Number of other classes referenced by the class
    - NOA - Number Of Attributes
    - NOPA - Number of Public Attributes
    - NOPRA - Number of Private Attributes
    - NOAI - Number of Attributes Inherited
    - LOC - Number of Lines of Code
    - NOM - Number of Methods
    - NOPM - Number of Public Methods
    - NOPRM - Number of Private Methods
    - NOMI - Number of Methods Inherited
    - Ca - Afferent Couplings
    - Ce - Efferent Couplings
    
- McCabe
    - Maximum Cabe's Cyclomatic Complexity
    - Average Cane's Cyclomatic Complexity
#### Process Metrics

#### Entropy

### Method Granularity
| metrics |
| ------- |
| Anonymous_inner_class_length |
| Boolean_expression_complexity |
| CC |
| Class_Data_Abstraction_Coupling |
| Class_Fan-Out_Complexity |
| Cyclomatic_Complexity |
| Executable_statement_count |
| File_length |
| LOC |
| Method_length |
| NCSS_for_this_class |
| NCSS_for_this_file |
| NCSS_for_this_method |
| NPath_Complexity |
| Nested_for_depth |
| Nested_if-else_depth |
| Nested_try_depth |
| Number_of_package_methods |
| Number_of_private_methods |
| Number_of_protected_methods |
| Number_of_public_methods |
| PC |
| Return_count |
| Throws_count |
| Total_number_of_methods |
| anonymousClassesQty |
| assignmentsQty |
| cbo |
| comparisonsQty |
| constructor |
| innerClassesQty |
| lambdasQty |
| loc |
| logStatementsQty |
| loopQty |
| mathOperationsQty |
| maxNestedBlocks |
| modifiers |
| numbersQty |
| parameters |
| parenthesizedExpsQty |
| returns |
| rfc |
| stringLiteralsQty |
| tryCatchQty |
| uniqueWordsQty |
| variables |
| wmc |

WMC + Smells
Designite vs Fowler

## Metrics
| category | subcategory | metric | description | implemented | tool |
| -------- | ----------- | ------ | ----------- | ----------- | ---- |
| product | CK | WMC | Weighted Method Count | :white_check_mark: | | 
| product | CK | DIT | Depth of Inheritance Tree | :white_check_mark: | | 
| product | CK | RFC | Response For Class | :white_check_mark: | | 
| product | CK | NOC | Number of Children | :white_check_mark: | | 
| product | CK | CBO | Coupling Between Objects | :white_check_mark: | |
| product | CK | LCOM | Lack of Cohesion in Methods | :white_check_mark: | |
| product | OO | FanIn | Number of other classes that reference the class | :white_check_mark: | |
| product | OO | FanOut | Number of other classes referenced by the class | :white_check_mark: | |
| product | OO | NOA | Number Of Attributes | :x: | |
| product | OO | NOPA | Number of Public Attributes | :x: | |
| product | OO | NOPRA | Number of Private Attributes | :x: | |
| product | OO | NOAI | Number of Attributes Inherited | :x: | |
| product | OO | LOC | Number of Lines of Code | :white_check_mark: | |
| product | OO | NOM | Number of Methods | :white_check_mark: | |
| product | OO | NOPM | Number of Public Methods | :white_check_mark: | |
| product | OO | NOPRM | Number of Private Methods | :white_check_mark: | |
| product | OO | NOMI | Number of Methods Inherited | :white_check_mark: | |
| product | OO | Ca | Afferent Couplings | :x: | |
| product | OO | Ce | Efferent Couplings | :x: | |
| product | McCabe | Max(CC) | Maximum Cabe's Cyclomatic Complexity | :x: | |
| product | McCabe | Avg(CC) | Average Cane's Cyclomatic Complexity | :x: | |
| process | Moser | REVISION | Number of revisions of a file | :x: | |
| process | Moser | REFACTORINGS | Number of times a file has been refactored | :x: | |
| process | Moser | BUGFIXES | Number of times a file was involved in bug-fixing | :x: | |
| process | Moser | AUTHORS | Number of distinct authors that checked a file into the repository | :x: | |
| process | Moser | LOC_ADDED | Sum over all revisions of the lines of code added to a file | :x: | |
| process | Moser | MAX_LOC_ADDED | Maximum number of lines of code added for all revisions | :x: | |
| process | Moser | AVE_LOC_ADDED | Average lines of code added per revision | :x: | |
| process | Moser | LOC_DELETED | Sum over all revisions of the lines of code deleted from a file | :x: | |
| process | Moser | MAX_LOC_DELETED | Maximum number of lines of code deleted for all revisions | :x: | |
| process | Moser | AVE_LOC_DELETED | Average lines of code deleted per revision | :x: | |
| process | Moser | CODECHURN | Sum of (added lines of code – deleted lines of code) over all revisions Maximum CODECHURN for all revisions | :x: | |
| process | Moser | MAX_CODECHURN | Maximum CODECHURN for all revisions | :x: | |
| process | Moser | AVE_CODECHURN | Average CODECHURN per revision | :x: | |
| process | Moser | MAX_CHANGESET | Maximum number of files committed together to the repository | :x: | |
| process | Moser | AVE_CHANGESET | Average number of files committed together to the repository | :x: | |
| process | Moser | AGE WEIGHTED_AGE | Age of a file in weeks (counting backwards from a specific release) See equation (1) | :x: | |
