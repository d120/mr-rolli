from src.database import Database
from src.model import UserLanguage


TEXT_UNIVERSAL = {
        'welcome': '''Hallo Ersti und willkommen auf dem Discord-Server der Informatik-Ophase!
Hello fellow student and welcome to the Discord server of the introduction week for computer science!

Bitte wähle die von dir gewünschte Sprache aus:
Please select your preferred language:'''
}
TEXT_GERMAN = {
        'language-set': 'Deine Sprache wurde auf „Deutsch“ eingestellt!'
}
TEXT_ENGLISH = {
        'language-set': 'Your language for set to “English”!'
}



class I18n:
    def __init__(self, database: Database):
        self._database = database


    def get_text(self, discord_username: str, id: str):
        if id in TEXT_UNIVERSAL:
            return TEXT_UNIVERSAL[id]

        user_info = self._database.get_user_info(discord_username)
        language = user_info.language
        if language is None:
            raise Exception(f'A non-universal text {id=} was requested, but the user {discord_username=} does not have a specified language!')
        if language == UserLanguage.GERMAN:
            return TEXT_GERMAN[id]
        elif language == UserLanguage.ENGLISH:
            return TEXT_ENGLISH[id]
        raise Exception(f'Cannot find translated text {id=} for language {language=}!')
