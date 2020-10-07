import os

from apscheduler.schedulers.background import BackgroundScheduler

from src.discord_bot import DiscordBot
from src.pretix_api import PretixApi
from src.pretix_cache import PretixCache


refresh_every_n_minutes = 60

pretix_auth_token = os.getenv('PRETIX_AUTH_TOKEN')
if not pretix_auth_token:
    raise Exception('Please set the environment variable PRETIX_AUTH_TOKEN to the pretix authentication token.')

discord_auth_token = os.getenv('DISCORD_AUTH_TOKEN')
if not discord_auth_token:
    raise Exception('Please set the environment variable DISCORD_AUTH_TOKEN to the discord authentication token.')



def refresh_pretix_cache():
    print('Performing pretix refresh.')
    cache.refresh()
    print('Finished!')



print('Setting up pretix cache.')
cache = PretixCache(PretixApi('https://anmeldung.d120.de', pretix_auth_token), 'ophase', 'ws-2020-21')
refresh_pretix_cache()

print(f'Setting up scheduler to refresh cache every {refresh_every_n_minutes} minutes.')
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_pretix_cache, 'interval', minutes = refresh_every_n_minutes)
scheduler.start()

print('Starting Discord bot.')
bot = DiscordBot(cache)
bot.run(discord_auth_token)
