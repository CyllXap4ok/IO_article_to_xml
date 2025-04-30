from dataclasses import dataclass, field
from data.author import Author
from data.enum_const import Language, ArticleType, Code

@dataclass
class ArticleDataLang:
    """Класс, содержащий информацию из статьи на определенном языке

    Attributes:
        title (str): Заголовок статьи
        abstract (str): Аннотация статьи
        keywords (list(str)): Список ключевых слов
        text (str): Текст статьи от Introduction до References
        funding (str): Финансирование. Находится в статье под заголовком Acknowledgements
    """
    title: str = '' # готов ENG
    abstract: str = '' # готово ENG
    keywords: list[str] = field(default_factory=list)  # готов ENG
    text: str = ''  # готово
    funding: str = ''  # готов ENG


@dataclass
class ArticleData:
    """Класс, содержащий общую информацию из статьи

        Attributes:
            pages (str): Номера страниц статьи в выпуске в формате Num-Num или Num
            article_type (ArticleType): Тип статьи
            codes (dict(Code, str)): Коды статьи (UDK, EDN, DOI...)
            authors (list(Author)): Список авторов статьи, включая рецензентов
            __languages (dict(Language, ArticleDataLang)): Словарь, содержащий информацию статьи для каждого языка.
    """
    received_date: str = '' # готово
    accepted_date: str = '' # готово
    authors: list[Author] = field(default_factory=list)  # готово
    pages = '' # готово
    article_type = ArticleType.UNK  # СДЕЛАТЬ. Брать из строгой формы essential information
    codes: dict[Code, str | list[str]] = field(default_factory=dict)  # СДЕЛАТЬ. Брать из строгой формы essential information
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
