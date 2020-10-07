import discord

from src.constants import Products, Programs
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
    def __init__(self, cache: PretixCache):
        super().__init__(intents = discord.Intents(members = True))

        self._cache = cache


    async def on_ready(self):
        print(f'Discord bot ready as {self.user}.')


    async def on_member_join(self, member):
        # TODO: Maybe send the member a message? Nadja+Communicator.
        user_info = self._cache.get_user_info(member.name, member.discriminator)
        if user_info is None:
            await member.send('Hello there! Sadly, we could not find any information about your Discord ID. Please contact someone to get assigned the correct roles.')
            return
        product, programs = user_info
        roles = []
        if product == Products.MASTER:
            roles.append(DiscordRole(MASTER_ERSTI_ROLE_ID))
        for program in programs:
            roles.append(DiscordRole(PROGRAMS_MAP[program]))
        await member.add_roles(*roles, reason = 'Import from Pretix.', atomic = True)


    async def on_message(self, message):
        print('Message from %s: %s' % (message.author, message.content))
