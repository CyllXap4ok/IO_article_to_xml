from enum import Enum

class Language(Enum):
    RUS = 'Русский'
    ENG = 'Английский'

class ArticleType(Enum):
    ABS = 'Abstract'
    BRV = 'Review'
    CNF = 'Conference Report, Theses of Report'
    COR = 'Correspondence'
    EDI = 'Editorial'
    MIS = 'Miscellaneous'
    PER = 'Personal'
    RAR = 'Research Article'
    REP = 'Scientific Report'
    REV = 'Review Article'
    RPR = 'Reprint'
    SCO = 'Short Communication'
    UNK = 'Unknown'

class AuthorRole(Enum):
    Default = ''
    Corresponding = '1'
    Reviewer = '23'

class Code(Enum):
    DOI = 'doi'
    UDK = 'udk'
    rubric = 'rubric'