"""Модуль стратегий сохранения

   При добавлении новой стратегии обязательно добавить её в enum SavingStrategies в конце файла!
"""

import xml.etree.ElementTree as XMLT

from abc import ABC, abstractmethod
from enum import Enum
from xml.etree.ElementTree import Element
from xml.dom import minidom

from data.article import ArticleData
from data.author import Author
from data.enum_const import Language, AuthorRole


class DataSavingStrategy(ABC):

    @abstractmethod
    def save_data(self, saving_path: str, data: ArticleData):
        pass


class DocxSavingStrategy(DataSavingStrategy):

    def save_data(self, saving_path: str, data: ArticleData):
        path = saving_path + '.docx'


class XMLSavingStrategy(DataSavingStrategy):

    def save_data(self, saving_path: str, data: ArticleData):
        path = saving_path + '.xml'

        article = XMLT.Element('article')

        pages = XMLT.SubElement(article, 'pages')
        pages.text = ''

        self.__add_authors(article, data.authors)

        art_type = XMLT.SubElement(article, 'artType')
        art_type.text = "ОБЯЗАТЕЛЬНЫЙ элемент"

        lang_publ = XMLT.SubElement(article, "langPubl")
        lang_publ.text = "ВАРИАТИВНЫЙ элемент"

        for parent, tag, attr in [
            (XMLT.SubElement(article, 'artTitles'), 'artTitle', 'title'),
            (XMLT.SubElement(article, 'abstracts'), 'abstract', 'abstract'),
            (XMLT.SubElement(article, 'fundings'), 'funding', 'funding')
        ]:
            for lang in Language:
                if value := getattr(data[lang], attr):
                    XMLT.SubElement(parent, tag, lang=lang.name).text = value

        self.__create_readable_xml(article, path)

    @staticmethod
    def __create_lang_sub_elements(parent: Element, tag: str) -> dict[Language, Element]:
        return {
            lang: XMLT.SubElement(parent, tag, lang=lang.name)
            for lang in Language
        }

    def __add_authors(self, parent: Element, authors: [Author]):
        authors_el = XMLT.SubElement(parent, 'authors')
        for num, author in enumerate(authors, 1):
            author_el = XMLT.SubElement(authors_el, 'author', num=str(num))

            individual_info = self.__create_lang_sub_elements(author_el, 'individInfo')

            match author.role:
                case (AuthorRole.Reviewer):
                    XMLT.SubElement(author_el, 'role').text = author.role.value
                    XMLT.SubElement(individual_info[Language.RUS], 'comment').text = author[Language.RUS].review
                case (AuthorRole.Corresponding):
                    XMLT.SubElement(author_el, 'correspondent').text = author.role.value

            self.__add_author_lang_elements(individual_info, 'surname', author)
            self.__add_author_lang_elements(individual_info, 'initials', author)
            self.__add_organisations(individual_info, author)

    @staticmethod
    def __add_author_lang_elements(parents: dict[Language, Element], attr: str, author: Author):
        for lang, parent in parents.items():
            XMLT.SubElement(parent, attr).text = getattr(author[lang], attr)

    @staticmethod
    def __add_organisations(parents: dict[Language, Element], author: Author):
        for lang, parent in parents.items():
            if author[lang].workplaces:
                towns, countries, names = zip(*[
                    (workplace.town, workplace.country, workplace.name)
                    for workplace in author[lang].workplaces
                ])

                XMLT.SubElement(parent, 'town').text = '; '.join(towns)
                XMLT.SubElement(parent, 'country').text = '; '.join(countries)
                XMLT.SubElement(parent, 'orgName').text = '; '.join(names)

    @staticmethod
    def __create_readable_xml(article: Element, path: str):
        xml_string = XMLT.tostring(article, encoding="utf-8")
        readable_xml = minidom.parseString(xml_string).toprettyxml(indent='  ')
        with open(path, "w", encoding="utf-8") as f:
            f.write(readable_xml)


class SavingStrategies(Enum):
    """Список стратегий

       Для добавления новой надо создать свойство по правилу:
       расширение = DataSavingStrategy()
    """
    docx = DocxSavingStrategy()
    xml = XMLSavingStrategy()
