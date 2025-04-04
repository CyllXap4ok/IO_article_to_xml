from dataclasses import dataclass, field
from author import Author
from common import Language, ArticleType, Code

@dataclass
class ArticleDataLang:
    title: str = ''
    abstract: str = ''
    keywords: list[str] = field(default_factory=list)  # готово
    text: str = ''  # готово
    funding = ''  # готово


@dataclass
class ArticleData:
    pages = ''
    article_type = ArticleType.UNK
    codes: dict[Code, str | list[str]] = field(default_factory=dict) # СДЕЛАТЬ. Брать из строгой формы essential information
    authors: list[Author] = field(default_factory=list)  # готово
    __languages: dict[Language, ArticleDataLang] = field(default_factory=dict)

    def __getitem__(self, lang: Language):
        if lang not in self.__languages:
            self.__languages[lang] = ArticleDataLang()
        return self.__languages[lang]

    def __setitem__(self, lang: Language, article_data_lang: ArticleDataLang):
        self.__languages[lang] = article_data_lang

    def clear(self): self.__init__()

    def get_languages(self):
        return ','.join([lang.name for lang in self.__languages.keys()])