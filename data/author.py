from dataclasses import dataclass, field
from enum_const import Language, AuthorRole
from workplace import Workplace


@dataclass
class AuthorLang:
    surname = ''
    initials = ''
    workplaces: list[Workplace] = field(default_factory=list)
    _role: AuthorRole = AuthorRole.Default
    __review: str = field(default=None, init=False)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role: AuthorRole):
        self._role = role

    @property
    def review(self):
        if self._role == AuthorRole.Reviewer:
            return self.__review
        else:
            return "Error: this author has no review. Authos status is not Reviewer"

    @review.setter
    def review(self, review: str):
        if self._role == AuthorRole.Reviewer:
            self.__review = review
        else:
            raise PermissionError("It's not possible to assign a review to an author whose status is not Reviewer")


@dataclass
class Author:
    __languages: dict[Language, AuthorLang] = field(default_factory=dict)
    _role = AuthorRole.Default

    def __getitem__(self, lang: Language):
        if lang not in self.__languages:
            self.__languages[lang] = AuthorLang(_role=self.role)
        return self.__languages[lang]

    def __setitem__(self, lang: Language, author_lang: AuthorLang):
        self.__languages[lang] = author_lang

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role: AuthorRole):
        self._role = role
        for author_lang in self.__languages.values():
            author_lang.role = role

    def get_languages(self):
        return ','.join([lang.name for lang in self.__languages.keys()])