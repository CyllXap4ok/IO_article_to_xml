from dataclasses import dataclass
import re


@dataclass
class Workplace:
    name: str = ''
    town: str = ''
    country: str = ''

    class Builder:

        def __init__(self):
            self._workplace = Workplace()

        def parse(self, workplace_text: str) -> "Workplace.Builder":
            text_parts = [part.strip(' ') for part in workplace_text.split(',')]
            is_workplace_name = True

            for part in text_parts:
                if self._is_address_part(part):
                    is_workplace_name = False
                    continue

                if is_workplace_name:
                    self._workplace.name += part + ', '
                else:
                    if not part.startswith(tuple('0123456789')):
                        self._workplace.town += part + ', '
                    else:
                        self._workplace.country += part.strip('0123456789 ')

            self._clean_fields()
            return self

        @staticmethod
        def _is_address_part(part: str):
            return (part.endswith(tuple('0123456789')) or
                    (bool(re.search(r'\d', part)) and '.' in part))

        def _clean_fields(self):
            self._workplace.name = self._workplace.name.strip(', ')
            self._workplace.town = self._workplace.name.strip(', ')
            self._workplace.country = self._workplace.name.strip(', ')

        def build(self) -> "Workplace":
            return self._workplace