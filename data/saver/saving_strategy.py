"""Модуль стратегий сохранения"""

import xml.etree.ElementTree as XMLT

from abc import ABC, abstractmethod
from html import escape
from xml.etree.ElementTree import Element
from xml.dom import minidom

from data.article import ArticleData
from data.author import Author
from data.enum_const import Language, AuthorRole
from data.workplace import Workplace


class DataSavingStrategy(ABC):

    @abstractmethod
    def save_data(self, saving_path: str, data: ArticleData):
        pass


class DocxSavingStrategy(DataSavingStrategy):

    def save_data(self, saving_path: str, data: ArticleData):
        path = saving_path + '.docx'


class XMLSavingStrategy(DataSavingStrategy):

    def save_data(self, saving_path: str, data: ArticleData):
        article = self.__create_article_xml(data)
        self.__save_xml(element=article, path=saving_path + '.xml')

    def __create_article_xml(self, data: ArticleData) -> Element:

        article = XMLT.Element('article')

        XMLT.SubElement(article, 'pages').text = data.pages
        XMLT.SubElement(article, 'artType').text = data.article_type.name
        XMLT.SubElement(article, "langPubl").text = "ВАРИАТИВНЫЙ элемент"

        self.__add_authors(article, data.authors)

        art_titles_el = XMLT.SubElement(article, 'artTitles')
        abstracts_el = XMLT.SubElement(article, 'abstracts')

        for lang in (Language.ENG, Language.RUS):
            if text := data[lang].text:
                XMLT.SubElement(article, 'text', lang=lang.name).text = text

        codes_el = XMLT.SubElement(article, 'codes')

        for code_type, codes_list in data.codes.items():
            XMLT.SubElement(codes_el, code_type.name.lower()).text = '; '.join(codes_list)

        keywords = XMLT.SubElement(article, 'keywords')

        rubrics = XMLT.SubElement(article, 'rubrics')

        for rubric in data.rubrics:
            XMLT.SubElement(rubrics, 'rubric').text = rubric

        dates = XMLT.SubElement(article, 'dates')
        XMLT.SubElement(dates, 'dateReceived').text = data.received_date
        XMLT.SubElement(dates, 'dateAccepted').text = data.accepted_date

        fundings_el = XMLT.SubElement(article, 'fundings')

        for lang in (Language.ENG, Language.RUS):
            XMLT.SubElement(art_titles_el, 'artTitle', lang=lang.name).text = data[lang].title
            XMLT.SubElement(abstracts_el, 'abstract', lang=lang.name).text = data[lang].abstract
            XMLT.SubElement(fundings_el, 'funding', lang=lang.name).text = data[lang].funding

            kwd_group = XMLT.SubElement(keywords, 'kwdGroup', lang=lang.name)
            for keyword in data[lang].keywords:
                XMLT.SubElement(kwd_group, 'keyword').text = escape(keyword)

        return article

    def __add_authors(self, parent: Element, authors: [Author]):

        authors_el = XMLT.SubElement(parent, 'authors')

        for num, author in enumerate(authors, 1):

            author_el = XMLT.SubElement(authors_el, 'author', num=str(num))

            if author.role is AuthorRole.Corresponding:
                XMLT.SubElement(author_el, 'correspondent').text = author.role.value
            else:
                XMLT.SubElement(author_el, 'role').text = author.role.value

            self.__add_individ_info(author_el, author, Language.ENG, Language.RUS)

    def __add_individ_info(self, author_el: Element, author: Author, *langs: Language):
        for lang in langs:
            individ_info = XMLT.SubElement(author_el, 'individInfo', lang=lang.name)

            XMLT.SubElement(individ_info, 'surname').text = author[lang].surname
            XMLT.SubElement(individ_info, 'initials').text = author[lang].initials

            self.__add_workplaces(individ_info, author[lang].workplaces)

            if author.role is AuthorRole.Reviewer and author[lang].review:
                XMLT.SubElement(individ_info, 'comment').text = author[lang].review

    @staticmethod
    def __add_workplaces(individ_info: Element, workplaces: list[Workplace]):

        town_el = XMLT.SubElement(individ_info, 'town')
        country_el = XMLT.SubElement(individ_info, 'country')
        org_name_el = XMLT.SubElement(individ_info, 'orgName')

        towns = [workplace.town for workplace in workplaces]
        countries = [workplace.country for workplace in workplaces]
        org_names = [workplace.name for workplace in workplaces]

        town_el.text = '; '.join(towns)
        country_el.text = '; '.join(countries)
        org_name_el.text = '; '.join(org_names)

    @staticmethod
    def __save_xml(element: Element, path: str):
        xml_string = XMLT.tostring(element, encoding="utf-8")
        readable_xml = minidom.parseString(xml_string).toprettyxml(indent='  ')
        with open(path, "w", encoding="utf-8") as f:
            f.write(readable_xml)
