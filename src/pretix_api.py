import math
import time
from typing import Generator, Optional

import requests

from logger_aware import LoggerAware

ApiResponse = dict[str, any]


class PretixApi(LoggerAware):
    PAGE_SIZE = 50

    def __init__(self, base_url: str, organizer: str, event_name: str, auth_token: str):
        super().__init__()
        self._api_url = f"{base_url}/api/v1"
        self._organizer = organizer
        self._event_name = event_name
        self._auth_token = auth_token

    def fetch_event(self) -> ApiResponse:
        return self._fetch_GET()

    def fetch_products(self) -> Generator[ApiResponse, None, None]:
        yield from self._fetch_all("/items")

    def fetch_questions(self) -> Generator[ApiResponse, None, None]:
        yield from self._fetch_all("/questions")

    def fetch_question(self, question_id: int) -> ApiResponse:
        return self._fetch_GET(f"/questions/{question_id}")

    def fetch_orders(self) -> Generator[ApiResponse, None, None]:
        yield from self._fetch_all("/orderpositions")

    def _fetch_all(self, path: str) -> Generator[ApiResponse, None, None]:
        page = 1
        total_pages = None
        while page is not None:
            if total_pages is None:
                self.logger.info(f"Requesting page {page:d}.")
            else:
                self.logger.info(f"Requesting page {page:d}/{total_pages:d}.")
            start = time.perf_counter()
            sublist, next_page, _, total_pages = self._fetch_paginated(path, page)
            end = time.perf_counter()
            self.logger.info(
                f"Finished request {page:d}/{total_pages:d}. Took {end - start:.1f}s."
            )
            yield from sublist
            page = next_page

    def _fetch_paginated(
        self, path: str, page: int
    ) -> tuple[list[ApiResponse], Optional[int], Optional[int], int]:
        result = self._fetch_GET(f"{path}?page={page}")
        has_next_page = bool(result["next"])
        has_previous_page = bool(result["previous"])
        max_pages = math.ceil(result["count"] / PretixApi.PAGE_SIZE)
        next_page = page + 1 if has_next_page else None
        previous_page = page - 1 if has_previous_page else None
        return result["results"], next_page, previous_page, max_pages

    def _fetch_GET(self, path: str = "") -> ApiResponse:
        url = f"{self._api_url}/organizers/{self._organizer}/events/{self._event_name}{path}"
        response = requests.get(
            url, headers={"Authorization": f"Token {self._auth_token}"}
        )
        assert (
            200 <= response.status_code < 400
        ), f"Unexpected response code {response.status_code} while GETting '{url}'."
        return response.json()
