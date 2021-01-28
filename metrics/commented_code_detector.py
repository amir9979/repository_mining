import os

RESERVED_WORDS = ['requires', 'try', 'dynamic_cast', 'module', 'sizeof', 'synchronized', 'delete', 'goto', 'interface',
                  'reinterpret_cast', 'wchar_t', 'switch', 'thread_local', 'char16_t', 'struct', 'xor_eq', 'noexcept',
                  'break', 'union', 'return', 'private', 'protected', 'using', 'volatile', 'alignas', 'const_cast',
                  'assert', 'default', 'double', 'native', 'long', 'virtual', 'static', 'nullptr', 'bool', 'typeid',
                  'export', 'operator', 'xor', 'unsigned', 'asm', 'import', 'explicit', 'compl', 'class', 'instanceof',
                  'boolean', 'byte', 'var', 'auto', 'new', 'inline', 'else', 'and', 'or', 'do', 'final', 'transient',
                  'abstract', 'short', 'register', 'finally', 'for', 'not_eq', 'exports', 'alignof', 'char', 'throw',
                  'not', 'template', 'char32_t', 'while', 'static_assert', 'continue', 'implements', 'float', 'if',
                  'int', 'and_eq', 'public', 'decltype', 'extern', 'true', 'typename', 'case', 'static_cast', 'bitand',
                  'const', 'catch', 'typedef', 'package', 'super', 'void', 'mutable', 'strictfp', 'friend', 'enum',
                  'signed', 'or_eq', 'bitor', 'false', 'extends', 'constexpr', 'namespace', 'this', 'throws']

# Note that the order of the list PURE_OPERATORS is important, because
# because matching is being done from the begining of the list to the end.
PURE_OPERATORS = [
    "::", "++", "--", "(", ")", "[", "]", ".", "->", "++", "--", "+", "-", 
    "!", "~", "*", "&", ".*", "->*", "*", "/", "%", "+", "-", "<<", ">>", 
    "<", "<=", ">", ">=", "==", "!=", "&", "^", "|", "&&", "||", "?:", "=", 
    "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=", ",", "\"", 
    "\'", "\\", ";", "{", "}"
    ]

# Comment tokens
ONELINE_COMMENT_TOKEN = "//"
MULTILINE_COMMENT_TOKEN_BEGIN = "/*"
MULTILINE_COMMENT_TOKEN_END = "*/"


import math

class Comment:
    def __init__(self):
        self.content = ""
        self.firstLineNumber = -1
        self.lastLineNumber = -1    
        
        
    def addContent(self, appendedContent, lineNumber):
        self.content = " ".join([self.content, appendedContent])
        self.lastLineNumber = lineNumber
        if self.firstLineNumber == -1:
            self.firstLineNumber = lineNumber
        
        
    def isEmpty(self):
        return self.firstLineNumber == -1
        
        
    def getContent(self):
        return self.content
        
        
    def getFirstLineNumber(self):
        return self.firstLineNumber
        
        
    def getLastLineNumber(self):
        return self.lastLineNumber
        
        
    def getLength(self):
        return self.getLastLineNumber() - self.getFirstLineNumber() + 1
        
        
    def newLine(self):
        self.content += "\n"
        
        
    def __str__(self):
        return "Comment from lines %d-%d:\n%s" %(self.getFirstLineNumber(),
            self.getLastLineNumber(), self.getContent())


class HalsteadSourceLine:
    def __init__(self, line, line_number):
        self.line = line
        self.line_number = line_number
        self.operandsCnt = 0
        self.operatorsCnt = 0
        self.operands = set()
        self.operators = set()

        self.analyze()

    def analyze(self):
        for lexem in self.line.split():
            self._analyzeLexem(lexem)

    def _analyzeLexem(self, lexem):
        reduct = lexem
        while reduct:
            reduct = self._reduceLexem(reduct)

    def _reduceLexem(self, lexem):
        nonPureShortestPrefixLen = len(lexem)
        for operator in PURE_OPERATORS:
            if lexem.startswith(operator):
                self.operatorsCnt += 1
                self.operators.add(operator)
                return lexem[len(operator):]
            if operator in lexem:
                nonPureShortestPrefixLen = min(
                    nonPureShortestPrefixLen,
                    lexem.find(operator)
                )
        nonPureShortestPrefix = lexem[:nonPureShortestPrefixLen]
        for keyword in RESERVED_WORDS:
            if nonPureShortestPrefix == keyword:
                self.operatorsCnt += 1
                self.operators.add(keyword)
                return lexem[nonPureShortestPrefixLen:]
        self.operandsCnt += 1
        self.operands.add(nonPureShortestPrefix)
        return lexem[nonPureShortestPrefixLen:]

    def getDistinctOperatorsCnt(self):
        return len(self.operators)

    def getDistinctOperandsCnt(self):
        return len(self.operands)

    def getTotalOperatorsCnt(self):
        return self.operatorsCnt

    def getTotalOparandsCnt(self):
        return self.operandsCnt

    def getLength(self):
        return self.getTotalOperatorsCnt() + self.getTotalOparandsCnt()

    def getVocabulary(self):
        return self.getDistinctOperatorsCnt() + self.getDistinctOperandsCnt()

    def getVolume(self):
        return self.getLength() * math.log(unzero(self.getVocabulary()), 2)

    def getDifficulty(self):
        return (self.getDistinctOperatorsCnt() / 2 *
                self.getTotalOparandsCnt() / unzero(
                    self.getDistinctOperandsCnt()))

    def getEffort(self):
        return self.getDifficulty() * self.getVolume()

    def getValuesVector(self):
        return {
            "getTotalOperatorsCnt" : self.getTotalOperatorsCnt(),
            "getDistinctOperatorsCnt": self.getDistinctOperatorsCnt(),
            "getTotalOparandsCnt": self.getTotalOparandsCnt(),
            "getDistinctOperandsCnt": self.getDistinctOperandsCnt(),
            "getLength": self.getLength(),
            "getVocabulary" : self.getVocabulary(),
            "getVolume": self.getVolume(),
            "getDifficulty": self.getDifficulty(),
            "getEffort": self.getEffort()
        }


class Halstead:
    def __init__(self, sourcelines):
        self.operandsCnt = 0
        self.operatorsCnt = 0
        self.operands = set()
        self.operators = set()
        
        for line in sourcelines:
            self.operandsCnt += line.operandsCnt
            self.operatorsCnt += line.operatorsCnt
            self.operands = self.operands.union(line.operands)
            self.operators = self.operators.union(line.operators)
    
    def getDistinctOperatorsCnt(self):
        return len(self.operators)

    def getDistinctOperandsCnt(self):
        return len(self.operands)
    
    def getTotalOperatorsCnt(self):
        return self.operatorsCnt
    
    def getTotalOparandsCnt(self):
        return self.operandsCnt
    
    def getLength(self):
        return self.getTotalOperatorsCnt() + self.getTotalOparandsCnt()
    
    def getVocabulary(self):
        return self.getDistinctOperatorsCnt() + self.getDistinctOperandsCnt()
        
    def getVolume(self):
        return self.getLength() * math.log(unzero(self.getVocabulary()), 2)
    
    def getDifficulty(self):
        return (self.getDistinctOperatorsCnt() / 2 * 
            self.getTotalOparandsCnt() / unzero(
                self.getDistinctOperandsCnt()))

    def getEffort(self):
        return self.getDifficulty() * self.getVolume()

    def getValuesVector(self):
        return {
            "HalsteadTotalOperatorsCnt" : self.getTotalOperatorsCnt(),
            "HalsteadDistinctOperatorsCnt": self.getDistinctOperatorsCnt(),
            "HalsteadTotalOparandsCnt": self.getTotalOparandsCnt(),
            "HalsteadDistinctOperandsCnt": self.getDistinctOperandsCnt(),
            "HalsteadLength": self.getLength(),
            "HalsteadVocabulary" : self.getVocabulary(),
            "HalsteadVolume": self.getVolume(),
            "HalsteadDifficulty": self.getDifficulty(),
            "HalsteadEffort": self.getEffort()
        }

    @staticmethod
    def printStatistics(valuesVectors, headers=None):
        names = ["Operators count:", "Distinct operators:", "Operands count:",
        "Distinct operands:", "Program length:", "Program vocabulary:",
        "Volume:", "Difficulty:", "Effort"]
        
        if headers:
            output = "".ljust(22)
            for header in headers:
                output += header.ljust(10)
            print(output)

        for i in range(len(names)):
            output=names[i].ljust(22)
            for vector in valuesVectors:                
                output += ("%.2f" %(vector[i])).ljust(10)
            print(output)


class CommentFilter:
    def filterComments(self, source):
        """ 
            @input: list of lines of file
            @return: tuple containing list of lines of file and list of 
                Comments
        """
        self.regularLines = []
        self.comments = []
        self.inMultilineComment = False
        self.currentComment = Comment()
        self.lineNumber = 0
    
        for line in source:
            self.currentLine = []
            _line = str(line)
            while _line:
                _line = self.reduceLine(_line)
            self.regularLines.append(HalsteadSourceLine(" ".join(self.currentLine), self.lineNumber))
            self.lineNumber += 1
            if not self.currentComment.isEmpty():
                self.currentComment.newLine()
        
        if not self.currentComment.isEmpty():
            self.comments.append(self.currentComment)
            self.currentComment = Comment()
        
        return (self.regularLines, self.comments)
    
    
    def reduceLine(self, line):
        notInLine = 999999
        multiLineBeginPosition = notInLine
        multiLineEndPosition = notInLine
        oneLinePosition = notInLine
        
        if MULTILINE_COMMENT_TOKEN_BEGIN in line:
            multiLineBeginPosition = line.find(MULTILINE_COMMENT_TOKEN_BEGIN)
            
        if MULTILINE_COMMENT_TOKEN_END in line:
            multiLineEndPosition = line.find(MULTILINE_COMMENT_TOKEN_END)
            
        if ONELINE_COMMENT_TOKEN in line:
            oneLinePosition = line.find(ONELINE_COMMENT_TOKEN)
        
        if (not self.inMultilineComment 
                and oneLinePosition < multiLineBeginPosition):
            self.currentLine.append(line[:oneLinePosition])
            self.currentComment.addContent(
                line[oneLinePosition + len(ONELINE_COMMENT_TOKEN):],
                self.lineNumber    
            )            
        elif self.inMultilineComment and multiLineEndPosition != notInLine:
            self.currentComment.addContent(
                line[:multiLineEndPosition],
                self.lineNumber
            )
            self.inMultilineComment = False
            return (line[multiLineEndPosition + 
                len(MULTILINE_COMMENT_TOKEN_END):])
        elif multiLineBeginPosition != notInLine:
            self.currentLine.append(line[:multiLineBeginPosition])
            self.inMultilineComment = True
            return (line[multiLineBeginPosition + 
                len(MULTILINE_COMMENT_TOKEN_BEGIN):])
        elif self.inMultilineComment:
            self.currentComment.addContent(line, self.lineNumber)
        else:
            if not self.currentComment.isEmpty():
                self.comments.append(self.currentComment)
                self.currentComment = Comment()
            self.currentLine.append(line)
        return ""


def unzero(v):
    if v == 0:
        return 0.00000001
    else:
        return v            


def metrics_for_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        source = f.read().splitlines()
        (regularLines, comments) = CommentFilter().filterComments(source)
    return Halstead(regularLines).getValuesVector()


def metrics_for_project(project_path):
    ans = {}
    for root, dirs, files in os.walk(project_path):
        for name in files:
            if name.endswith(".java"):
                full_path = os.path.normpath(os.path.join(root, name))
                ans[full_path[len(project_path)+1:]] = metrics_for_file(full_path)
    return ans
