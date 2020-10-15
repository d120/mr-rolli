import os

PRETIX_AUTH_TOKEN = os.getenv('PRETIX_AUTH_TOKEN')
if not PRETIX_AUTH_TOKEN:
    raise Exception('Please set the environment variable PRETIX_AUTH_TOKEN to the pretix authentication token.')

DISCORD_AUTH_TOKEN = os.getenv('DISCORD_AUTH_TOKEN')
if not DISCORD_AUTH_TOKEN:
    raise Exception('Please set the environment variable DISCORD_AUTH_TOKEN to the discord authentication token.')
