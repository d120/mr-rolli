import math
from typing import Dict, List, Optional, Tuple

import requests


class PretixApi:
    PAGE_SIZE = 50

    def __init__(self, base_url: str, auth_token: str):
        self._auth_headers = {'Authorization': f'Token {auth_token}'}
        self._base_url = base_url
        self._api_url = f'{self._base_url}/api/v1'

    def get_event(self, organizer: str, event_name: str) -> Dict[str, any]:
        return requests.get(f'{self._api_url}/organizers/{organizer}/events/{event_name}/', headers=self._auth_headers).json()

    def get_question(self, organizer: str, event_name: str, id: int) -> Dict[str, any]:
        return requests.get(f'{self._api_url}/organizers/{organizer}/events/{event_name}/questions/{id}/', headers=self._auth_headers).json()

    def get_orders(self, organizer: str, event_name: str, page: int = 1) -> Tuple[List[Dict[str, any]], Optional[int], Optional[int], int]:
        result = requests.get(f'{self._api_url}/organizers/{organizer}/events/{event_name}/orderpositions/?page={page}', headers=self._auth_headers).json()
        has_next_page = bool(result['next'])
        has_previous_page = bool(result['previous'])
        max_pages = math.ceil(result['count'] / PretixApi.PAGE_SIZE)
        next_page = page + 1 if has_next_page else None
        previous_page = page - 1 if has_previous_page else None
        return result['results'], next_page, previous_page, max_pages
