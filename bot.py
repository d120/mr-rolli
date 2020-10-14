from src.discord_bot import DiscordBot
from src.pretix_api import PretixApi
from src.pretix_cache import PretixCache
from src.tokens import DISCORD_AUTH_TOKEN, PRETIX_AUTH_TOKEN


print('Setting up pretix cache.')
cache = PretixCache(PretixApi('https://anmeldung.d120.de', PRETIX_AUTH_TOKEN), 'ophase', 'ws-2020-21')

print('Starting Discord bot.')
bot = DiscordBot(cache)
bot.run(DISCORD_AUTH_TOKEN)
