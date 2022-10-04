from dataclasses import dataclass

I18nString = dict[str, str]


@dataclass
class ProgramOption:
    identifier: str
    product_ids: list[int]
    options: dict[str, I18nString]


@dataclass
class Program:
    option: ProgramOption
    selected_options: list[I18nString]


@dataclass
class Product:
    id: int
    name: I18nString
    programs: list[ProgramOption]


@dataclass
class Order:
    code: str
    discord_username: str
    product: Product
    programs: list[Program]
    programming_course: bool
