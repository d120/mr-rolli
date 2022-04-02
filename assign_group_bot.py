import random
from typing import List

import discord
import numpy as np

from src import tokens
from src.discord_bot import DiscordRole


GUILD_ID = 854393229091668031
CHANNEL_ID = 854393229490520123
MESSAGE_ID = 897401386319380510
SUPPORTED_EMOJIS = ["pass"]
GROUPS = [
    {"id": 882195486608588800, "max_persons": 23},
    {"id": 882195774849572925, "max_persons": 23},
    {"id": 882195819145596978, "max_persons": 23},
    {"id": 882195846861574185, "max_persons": 23},
    {"id": 882195885860212788, "max_persons": 24},
    {"id": 882195915622977576, "max_persons": 23},
    {"id": 882195950746103848, "max_persons": 23},
    {"id": 882195987966353449, "max_persons": 23},
    {"id": 882196035366182942, "max_persons": 24},
    {"id": 882196066160766996, "max_persons": 23},
    {"id": 882196097668354068, "max_persons": 23},
    {"id": 882196140160876604, "max_persons": 23},
    {"id": 882196183026634802, "max_persons": 23},
    {"id": 882196231286304779, "max_persons": 23},
    {"id": 882196272029777930, "max_persons": 24},
    {"id": 882196464737091626, "max_persons": 24},
    {"id": 882196520257073182, "max_persons": 23},
    {"id": 896799682171379712, "max_persons": 23},
    {"id": 896851281799430144, "max_persons": 23},
    {"id": 897087987488280617, "max_persons": 24},
]


def format_user(user: discord.User) -> str:
    return user.name + "#" + user.discriminator


class GroupAssignmentBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents(members=True, messages=True, reactions=True))
        self._rng = np.random.default_rng()

    async def on_ready(self) -> None:
        print(f"Discord bot ready as {self.user}.")
        await self.do_work()
        print("Bot finished.")
        await self.close()
        print("Bot closed.")

    async def do_work(self) -> None:
        guild = await self.fetch_guild(GUILD_ID)
        await self.fetch_roles(guild)
        users = await self.extract_users(guild)
        groups = await self.distribute_users(users)
        await self.assign_roles(guild, groups)

    async def fetch_roles(self, guild: discord.Guild) -> None:
        await guild.fetch_roles()
        for group in GROUPS:
            group["name"] = list([role.name for role in guild.roles if role.id == group["id"]])[0]

    async def extract_users(self, guild: discord.Guild) -> List[discord.User]:
        print("Fetching channels.")
        channels = await guild.fetch_channels()
        channel = list(channel for channel in channels if channel.id == CHANNEL_ID)[0]

        print("Fetching message.")
        message = await channel.get_partial_message(MESSAGE_ID).fetch()

        result = []
        for reaction in message.reactions:
            name = getattr(reaction.emoji, "name", None)
            if name in SUPPORTED_EMOJIS:
                print(f"Fetching users that reacted with :{reaction.emoji.name}:.")
                users = await reaction.users().flatten()
                for user in users:
                    result.append(user)
                print(f"Fetched {len(users)} users.")
            else:
                print(f"Ignoring reactions with emoji {name}.")
        print(f"Fetched {len(result)} users in total.")
        return result

    async def distribute_users(self, users: List[discord.User]) -> List[List[discord.User]]:
        people = list(range(len(users)))
        groups = list([[] for _ in range(len(GROUPS))])
        full_groups = set()
        i = 0
        while len(people) > 0:
            group_idx = i % len(GROUPS)
            max_persons = GROUPS[group_idx]["max_persons"]
            if len(groups[group_idx]) < max_persons:
                person = random.choice(people)
                people.remove(person)
                groups[group_idx].append(users[person])
            else:
                print(f"Group {group_idx} is full, skipping.")
                full_groups.add(group_idx)
                if len(full_groups) >= len(groups):
                    print(f"All groups are full, but {len(people)} are left! Stopping assignment. People that are left: {', '.join(format_user(users[j]) for j in people)}")
                    break
            i += 1
        print("Finished group assignment:\n" + "\n".join(f"  Group {i:2d}: {', '.join(format_user(member) for member in members)}" for i, members in enumerate(groups)))
        return groups

    async def assign_roles(self, guild: discord.Guild, groups: List[List[discord.User]]):
        print("Fetching roles.")
        await guild.fetch_roles()

        print("Assigning roles.")
        for group_idx, users in enumerate(groups):
            group = GROUPS[group_idx]
            for user in users:
                print(f"Assigning {format_user(user)} role {group['name']} (ID {group['id']}).")
                member = await guild.fetch_member(user.id)
                await member.add_roles(DiscordRole(group['id']), atomic=True)


def main():
    GroupAssignmentBot().run(tokens.DISCORD_AUTH_TOKEN)


if __name__ == '__main__':
    main()
