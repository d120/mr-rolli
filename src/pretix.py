from typing import Iterable, Optional

import config
from logger_aware import LoggerAware
from model import Order, Product, Program, ProgramOption
from pretix_api import PretixApi
from timed_lru_cache import timed_lru_cache


class Pretix(LoggerAware):
    def __init__(self):
        super().__init__()
        self._api = PretixApi(config.pretix_url, config.pretix_organizer, config.pretix_event, config.pretix_auth_token)

    @timed_lru_cache()
    def load_order(self, discord_username: str) -> Optional[Order]:
        orders = self._load_orders()
        if discord_username not in orders:
            return None
        return orders[discord_username]

    @timed_lru_cache()
    def _load_orders(self) -> dict[str, Order]:
        orders = []
        for raw_order in self._api.fetch_orders():
            if raw_order["canceled"]:
                continue
            order = self._load_order(raw_order)
            if order is not None:
                orders.append(order)
        return {order.discord_username: order for order in orders}

    def _load_order(self, raw_order: dict[str, any]) -> Optional[Order]:
        code = raw_order["order"]
        discord_username = None
        products = self._load_products()
        if raw_order["item"] in products:
            product = products[raw_order["item"]]
        else:
            self.logger.warn(f"Unknown product ID {raw_order['item']} in order {code}.")
            return None
        programs = {}
        programming_course = False
        available_programs: dict[str, ProgramOption] = {program.identifier: program for program in product.programs}
        for answer in raw_order["answers"]:
            question_identifier = answer["question_identifier"]
            if question_identifier == config.pretix_discord_username:
                discord_username = "#".join([x.strip() for x in answer["answer"].split("#")])
                if "#" not in discord_username:
                    discord_username = None
            elif question_identifier in available_programs.keys():
                for opt in answer["option_identifiers"]:
                    option = available_programs[question_identifier]
                    if option.identifier not in programs:
                        programs[option.identifier] = Program(option, [])
                    programs[option.identifier].selected_options.append(option.options[opt])
            elif question_identifier == config.pretix_programming_course:
                programming_course = answer["answer"] == "True"
        programs = list(programs.values())
        if discord_username is None:
            return None
        return Order(code, discord_username, product, programs, programming_course)

    @timed_lru_cache()
    def _load_products(self) -> dict[int, Product]:
        # As we are using a lru_cache, we cannot return a generator here.
        products = {}
        programs = self._load_programs()
        for raw_product in self._api.fetch_products():
            if not raw_product["active"]:
                continue
            product_id = raw_product["id"]
            matching_programs = filter(lambda program: product_id in program.product_ids, programs)
            products[product_id] = Product(product_id, raw_product["name"], list(matching_programs))
        return products

    @timed_lru_cache()
    def _load_programs(self) -> Iterable[ProgramOption]:
        # As we are using a lru_cache, we cannot return a generator here.
        programs = []
        for raw_question in self._api.fetch_questions():
            if not raw_question["identifier"].endswith(config.pretix_programs_suffix):
                continue
            programs.append(ProgramOption(raw_question["identifier"], raw_question["items"], {option["identifier"]: option["answer"] for option in raw_question["options"]}))
        return programs
