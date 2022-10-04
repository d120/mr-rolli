import configparser
import os

config = configparser.ConfigParser()
config["DEFAULT"] = {
    "log_level": "INFO",
    "languages": "de-informal,en",
    "default_cache_time": "900",
}
config["PRETIX"] = {
    "url": "https://anmeldung.d120.de",
    "organizer": "pretix",
    "event": "pretix",
    "auth_token": "***** SECRET *****",
    "question_programs_suffix": "-programs",
    "question_discord_username": "discord-username",
    "question_programming_course": "programming-course",
}

if os.path.exists("config.ini"):
    config.read("config.ini")
with open("config.ini", "w") as f:
    config.write(f)

log_level = config["DEFAULT"]["log_level"]
languages = config["DEFAULT"]["languages"].split(",")
default_cache_time = int(config["DEFAULT"]["default_cache_time"])
pretix_url = config["PRETIX"]["url"]
pretix_organizer = config["PRETIX"]["organizer"]
pretix_event = config["PRETIX"]["event"]
pretix_auth_token = config["PRETIX"]["auth_token"]
pretix_programs_suffix = config["PRETIX"]["question_programs_suffix"]
pretix_discord_username = config["PRETIX"]["question_discord_username"]
pretix_programming_course = config["PRETIX"]["question_programming_course"]
__all__ = [
    # DEFAULT
    "log_level",
    "languages",
    "default_cache_time",
    # PRETIX
    "pretix_url",
    "pretix_organizer",
    "pretix_event",
    "pretix_auth_token",
    "pretix_programs_suffix",
    "pretix_discord_username",
    "pretix_programming_course",
]
