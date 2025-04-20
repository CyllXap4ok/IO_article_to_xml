from dataclasses import dataclass
import re


@dataclass
class Workplace:
    name: str = ''
    town: str = ''
    country: str = ''


class WorkplaceFactory:

    @staticmethod
    def create(workplace_text: str) -> Workplace:
        workplace = Workplace()
        # Место работы из статьи, разбитое по запятым
        workplace_text_parts = [part.strip(' ') for part in workplace_text.split(',')]
        is_workplace_name = True

        for part in workplace_text_parts:
            if part.endswith(tuple('0123456789')) or (bool(re.search(r'\d', part)) and '.' in part):
                is_workplace_name = False
                continue

            if is_workplace_name:
                workplace.name += part + ', '
            else:
                if not part.startswith(tuple('0123456789')):
                    workplace.town += part + ', '
                else:
                    workplace.country += part.strip('0123456789 ')

        workplace.name = workplace.name.strip(', ')
        workplace.town = workplace.town.strip(', ')
        workplace.country = workplace.country.strip(', ')
        return workplace