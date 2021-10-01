from time import time
from typing import Dict, List, Optional, Tuple

from src.database import Database
from src.model import Products, Programs, Order
from src.pretix_api import PretixApi

DISCORD_QUESTION_IDENTIFIER = 'discord-username'
BACHELOR_QUESTION_IDENTIFIER = 'bachelor-programs'
MASTER_QUESTION_IDENTIFIER = 'master-programs'
PROGRAMMING_COURSE_QUESTION_IDENTIFIER = 'programming-course'
PRODUCTS_MAP = {
    34: Products.MASTER,
    35: Products.BACHELOR
}
PROGRAMS_MAP = {
    # Bachelor programs.
    'XZ7HWBRS': Programs.BACHELOR_OF_SCIENCE,
    'WGXCU3EQ': Programs.BACHELOR_OF_EDUCATION,
    '3KNZDY7E': Programs.JOINT_BACHELOR_OF_ARTS,
    'ATXYY7W3': Programs.TEACHING_AT_SECONDARY_SCHOOLS,
    # Master programs.
    'KBHAADUT': Programs.AUTONOMOUS_SYSTEMS,
    'CQXCRPU7': Programs.DISTRIBUTED_SOFTWARE_SYSTEMS,
    'JHKHNZBK': Programs.UNIVERSAL,
    'DRE8WJPN': Programs.INTERNET_AND_WEBBASED_SYSTEMS,
    '88SDKLSA': Programs.IT_SECURITY,
    '3BYYM3PJ': Programs.VISUAL_COMPUTING
}


class PretixCache:
    def __init__(self, api: PretixApi, organizer: str, event_name: str):
        self._api = api
        self._organizer = organizer
        self._event_name = event_name

        self._db = Database()

    def refresh(self):
        raw_orders = self._fetch_raw_orders()
        for raw_order in raw_orders:
            order_info = self._extract_order_information(raw_order)
            if order_info is not None:
                discord_username, product, programs, programming_course = order_info
                self._db.insert_order(Order(discord_username, product, programs, programming_course), overwrite=True)

    def get_order(self, discord_username: str):
        return self._db.get_order(discord_username)

    def _extract_order_information(self, raw_order: Dict[str, any]) -> Optional[Tuple[str, Products, List[Programs], Optional[bool]]]:
        discord_username = None
        product = PRODUCTS_MAP[raw_order['item']]
        programs = []
        programming_course = None
        for answer in raw_order['answers']:
            question_identifier = answer['question_identifier']
            if question_identifier == DISCORD_QUESTION_IDENTIFIER:
                discord_username = '#'.join([x.strip() for x in answer['answer'].split('#')])
                if '#' not in discord_username:
                    discord_username = None
            elif question_identifier == BACHELOR_QUESTION_IDENTIFIER or question_identifier == MASTER_QUESTION_IDENTIFIER:
                for opt in answer['option_identifiers']:
                    programs.append(PROGRAMS_MAP[opt])
            elif question_identifier == PROGRAMMING_COURSE_QUESTION_IDENTIFIER:
                programming_course = answer['answer'] == 'True'
        if discord_username is None:
            return None
        return discord_username, product, programs, programming_course

    def _fetch_raw_orders(self) -> List[Dict[str, any]]:
        result = []
        page = 1
        total_pages = None
        while page is not None:
            if total_pages is None:
                print('Requesting page %d...' % page)
            else:
                # noinspection PyStringFormat
                print('Requesting page %d/%d...' % (page, total_pages))
            start = time()
            sublist, next_page, _, total_pages = self._api.get_orders(self._organizer, self._event_name, page=page)
            end = time()
            result += sublist
            print('Finished request %d/%d. Took %.1fs.' % (page, total_pages, end - start))
            page = next_page
        return result
