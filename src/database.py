import sqlite3
from typing import Optional

from src.model import Products, Programs, Order, UserInfo, UserLanguage, UserState


class Database:
    def __init__(self):
        self._conn = sqlite3.connect('database.sqlite')

        self._init_schema()

    def _init_schema(self):
        self._conn.execute('PRAGMA foreign_keys = ON')

        self._conn.execute('''CREATE TABLE IF NOT EXISTS orders (
                                  discord_username VARCHAR(256) NOT NULL,
                                  product_id INT NOT NULL,
                                  programming_course BOOLEAN NULL,
                                  PRIMARY KEY (discord_username)
                              )''')

        self._conn.execute('''CREATE TABLE IF NOT EXISTS orders_programs (
                                  discord_username VARCHAR(256) NOT NULL,
                                  program_id INT NOT NULL,
                                  PRIMARY KEY (discord_username, program_id),
                                  FOREIGN KEY (discord_username) REFERENCES orders (discord_username) ON DELETE CASCADE
                              )''')

        self._conn.execute('''CREATE TABLE IF NOT EXISTS user_info (
                                  discord_username VARCHAR(256) NOT NULL,
                                  state INT NOT NULL,
                                  LANGUAGE INT NULL,
                                  last_message_id INT NULL,
                                  PRIMARY KEY (discord_username)
                              )''')

        self._conn.execute('CREATE TABLE IF NOT EXISTS coc_decliners (discord_id INT PRIMARY KEY NOT NULL)')

        self._conn.commit()

    def insert_order(self, order: Order, overwrite: bool = False) -> bool:
        if next(self._conn.execute('SELECT COUNT(*) FROM orders WHERE discord_username = ?', [order.discord_username]))[0] > 0:
            if overwrite:
                self._conn.execute('DELETE FROM orders WHERE discord_username = ?', [order.discord_username])
            else:
                return False
        self._conn.execute('INSERT INTO orders (discord_username, product_id, programming_course) VALUES (?, ?, ?)',
                           [order.discord_username, order.product.value, order.programming_course])
        for program_id in order.programs:
            self._conn.execute('INSERT INTO orders_programs (discord_username, program_id) VALUES (?, ?) ON CONFLICT (discord_username, program_id) DO NOTHING',
                               [order.discord_username, program_id.value])
        self._conn.commit()
        return True

    def get_order(self, discord_username: str) -> Optional[Order]:
        query = '''SELECT
                       product_id,
                       programming_course,
                       op.program_id
                   FROM orders
                   INNER JOIN orders_programs op ON orders.discord_username = op.discord_username
                   WHERE
                       orders.discord_username = ?'''
        cursor = self._conn.execute(query, [discord_username])
        product_id, programming_course, programs = None, None, []
        for row in cursor:
            product_id, programming_course, program_id = row
            programs.append(Programs(program_id))
        if product_id is None:
            return None
        return Order(discord_username, Products(product_id), programs, programming_course)

    def set_user_info(self, discord_username: str, user_info: UserInfo) -> None:
        data = (user_info.state.value, None if user_info.language is None else user_info.language.value, user_info.last_message_id)
        self._conn.execute('INSERT INTO user_info (discord_username, state, language, last_message_id) VALUES (?, ?, ?, ?)' +
                           'ON CONFLICT (discord_username) DO UPDATE SET state = ?, language = ?, last_message_id = ?',
                           [discord_username, *data, *data])
        self._conn.commit()

    def get_user_info(self, discord_username: str) -> UserInfo:
        state, language, last_message_id = UserState.NEW, None, None
        for row in self._conn.execute('SELECT state, language, last_message_id FROM user_info WHERE discord_username = ?', [discord_username]):
            state = UserState(row[0])
            language = None if row[1] is None else UserLanguage(row[1])
            last_message_id = row[2]
        return UserInfo(state, language, last_message_id)

    def is_coc_decliner(self, discord_id: int) -> bool:
        return next(self._conn.execute('SELECT COUNT(*) FROM coc_decliners WHERE discord_id = ?', [discord_id]))[0] > 0

    def mark_coc_decliner(self, discord_id: int):
        self._conn.execute('INSERT INTO coc_decliners (discord_id) VALUES (?) ON CONFLICT DO NOTHING', [discord_id])
        self._conn.commit()
