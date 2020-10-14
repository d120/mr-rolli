from typing import Union

import discord

from src.constants import EMOJI_FLAG_DE, EMOJI_FLAG_US
from src.database import Database
from src.i18n import I18n
from src.model import Products, Programs, UserLanguage, UserState
from src.pretix_cache import PretixCache


MASTER_ERSTI_ROLE_ID = '740853171454214165'

PROGRAMS_MAP = { }
PROGRAMS_MAP[Programs.BACHELOR_OF_SCIENCE] = '712271886750318662'
PROGRAMS_MAP[Programs.BACHELOR_OF_EDUCATION] = '755822924132384798'
PROGRAMS_MAP[Programs.JOINT_BACHELOR_OF_ARTS] = '755822766091141192'
PROGRAMS_MAP[Programs.TEACHING_AT_SECONDARY_SCHOOLS] = '755823440358801429'
PROGRAMS_MAP[Programs.AUTONOMOUS_SYSTEMS] = '740852178247483463'
PROGRAMS_MAP[Programs.DISTRIBUTED_SOFTWARE_SYSTEMS] = '740852484880465950'
PROGRAMS_MAP[Programs.UNIVERSAL] = '712270706196611072'
PROGRAMS_MAP[Programs.INTERNET_AND_WEBBASED_SYSTEMS] = '740853615643590726'
PROGRAMS_MAP[Programs.IT_SECURITY] = '740853440925925426'
PROGRAMS_MAP[Programs.VISUAL_COMPUTING] = '740853857919303711'



class DiscordRole:
    def __init__(self, id: str):
        self.id = id


    def __repr__(self):
        return self.id


    def __str__(self):
        return self.id



class DiscordBot(discord.Client):
    def __init__(self, pretix_cache: PretixCache):
        super().__init__(intents = discord.Intents(members = True, messages = True, reactions = True))

        self._pretix_cache = pretix_cache
        self._database = Database()
        self._i18n = I18n(self._database)


    async def on_ready(self):
        print(f'Discord bot ready as {self.user}.')


    async def on_member_join(self, member: discord.Member):
        discord_username = self._get_discord_username(member)
        user_info = self._database.get_user_info(discord_username)
        if user_info.state == UserState.NEW:
            message = await member.send(self._i18n.get_text(discord_username, 'welcome'))
            await message.add_reaction(EMOJI_FLAG_DE)
            await message.add_reaction(EMOJI_FLAG_US)

            self._database.set_user_info(discord_username, user_info.next_state())

        # TODO: Revise from here on.
        order = self._pretix_cache.get_user_info(discord_username)
        if order is None:
            await member.send('Hello there! Sadly, we could not find any information about your Discord ID. Please contact someone to get assigned the correct roles.')
            return
        roles = []
        if order.product == Products.MASTER:
            roles.append(DiscordRole(MASTER_ERSTI_ROLE_ID))
        for program in order.programs:
            roles.append(DiscordRole(PROGRAMS_MAP[program]))
        await member.add_roles(*roles, reason = 'Import from Pretix.', atomic = True)


    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
        discord_username = self._get_discord_username(user)
        user_info = self._database.get_user_info(discord_username)
        if user_info.state == UserState.LANGUAGE_REQUESTED:
            emoji = reaction.emoji
            language = None
            if emoji == EMOJI_FLAG_DE:
                language = UserLanguage.GERMAN
            elif emoji == EMOJI_FLAG_US:
                language = UserLanguage.ENGLISH
            if language is not None:
                user_info.next_state()
                user_info.language = language
                self._database.set_user_info(discord_username, user_info)

                await user.send(self._i18n.get_text(discord_username, 'language-set'))


    async def on_message(self, message: discord.Message):
        if message.content == 'yikes':
            await self.on_member_join(message.author)


    def _get_discord_username(self, user: Union[discord.Member, discord.User]):
        return user.name + '#' + user.discriminator
