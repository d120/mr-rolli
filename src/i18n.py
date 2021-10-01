from src.constants import Emojis
from src.database import Database
from src.model import UserLanguage, Products, Programs

ORDER_FOUND_CONFIRM = 'order-found-confirm'
TEXT_SPECIAL = [ORDER_FOUND_CONFIRM]

TEXT_UNIVERSAL = {
    'welcome': '''Hallo Ersti und willkommen auf dem Discord-Server der Informatik-Ophase!
Hello fellow student and welcome to the Discord server of the introduction week for computer science!

Bitte wähle die von dir gewünschte Sprache aus:
Please select your preferred language:'''
}
TEXT_GERMAN = {
    'welcome-coc': f'''Herzlich Willkommen! Bitte lies die angehängte Willkommensnachricht und den Code of Conduct.

Akzeptierst du den Code of Conduct? Klicke {Emojis.YES} für ja und {Emojis.NO} für nein (du wirst dann nicht fortfahren können).''',
    'coc-accepted': 'Vielen Dank, dass du den CoC akzeptiert hast!',
    'coc-declined': 'Schade, dass du den Coc ablehnst. Du wirst alle Nachrichten auf dem Server lesen können, schreiben wird dir allerdings nicht erlaubt sein.',
    'language-set': 'Deine Sprache wurde auf „Deutsch“ eingestellt!',
    'order-not-found-select-product': 'Hast du dich in einen Informatik-Bachelor [1] oder einen Informatik-Master [2] eingeschrieben oder nimmst du nur am Programmiervorkurs teil [3]?',
    'ask-bachelor-program': '''In welchen der folgenden Bachelor-Studiengänge hast du dich eingeschrieben?
1. Bachelor of Science (B.Sc.)
2. Bachelor of Education (B.Ed.)
3. Joint Bachelor of Arts (JBA)
4. Lehramt an Gymnasien (LAG)
Solltest du dich in mehrere Bachelor-Studiengänge eingeschrieben haben, schreibe bitte eine Nachricht in #role-assignment.
''',
    'ask-master-program': '''In welche der folgenden Master-Studiengänge hast du dich eingeschrieben?
1. Autonome Systeme
2. Distributed Software Systems
3. Informatik (Allgemein)
4. Internet- und Web-basierte Systeme
5. IT-Sicherheit
6. Visual Computing
''',
    'ask-programming-course': 'Nimmst du am Programmiervorkurs teil?',
    'order-found-confirm-head': 'Wir konnten eine Anmeldung von dir finden 🙂',
    'order-found-confirm-bsc': 'Hast du dich in den Bachelor of Science (B.Sc.) eingeschrieben?',
    'order-found-confirm-bed': 'Hast du dich in den Bachelor of Education (B.Ed.) eingeschrieben?',
    'order-found-confirm-jba': 'Hast du dich in den Joint Bachelor of Arts (JBA) eingeschrieben?',
    'order-found-confirm-lag': 'Hast du dich in Lehramt an Gymnasien (LAG) eingeschrieben?',
    'order-found-confirm-msc': 'Hast du dich in die folgenden Master-Studiengänge eingeschrieben?',
    'msc-as': 'Autonome Systeme',
    'msc-dss': 'Distributed Software Systems',
    'msc-cs': 'Informatik (Allgemein)',
    'msc-dke': 'Internet- und Web-basierte Systeme',
    'msc-itsec': 'IT-Sicherheit',
    'msc-vc': 'Visual Computing',
    'roles-assigned': 'Dir wurden die entsprechenden Rollen zugewiesen. Viel Spaß!'
}
TEXT_ENGLISH = {
    'welcome-coc': f'''Welcome! Please read the attached welcome message and the code of conduct.

Do you accept the code of conduct? Press {Emojis.YES} for yes and {Emojis.NO} for no (you will not be able to continue).''',
    'coc-accepted': 'Thanks for accepting the CoC!',
    'coc-declined': 'Sadly you did decline the Coc. You will be able to read all messages but you will not be able to write any.',
    'language-set': 'Your language was set to “English”!',
    'order-not-found-select-product': 'Have you enrolled for a Computer Science Bachelor [1], Computer Science Master [2], or do you only take the programming course [3]?',
    'ask-bachelor-program': '''To which of the following bachelor programs are you enrolled?
1. Bachelor of Science (B.Sc.)
2. Bachelor of Education (B.Ed.)
3. Joint Bachelor of Arts (JBA)
4. Teaching at Secondary Schools (LAG)
If you are enrolled for multiple bachelor programs, please write a message in #role-assignment.
''',
    'ask-master-program': '''To which of the following master programs are you enrolled?
1. Autonomous Systems
2. Distributed Software Systems
3. Computer Science (Universal)
4. Internet- and Web-based Systems
5. IT-Security
6. Visual Computing
''',
    'ask-programming-course': 'Do you attend the programming course?',
    'order-found-confirm-head': 'We found a registration from you 🙂',
    'order-found-confirm-bsc': 'Are you enrolled for the Bachelor of Science?',
    'order-found-confirm-bed': 'Are you enrolled for the Bachelor of Education?',
    'order-found-confirm-jba': 'Are you enrolled for the Joint Bachelor of Arts?',
    'order-found-confirm-lag': 'Are you enrolled for Teaching at Secondary Schools (LAG)?',
    'order-found-confirm-msc': 'Are you enrolled for the following master programs?',
    'msc-as': 'Autonomous Systems',
    'msc-dss': 'Distributed Software Systems',
    'msc-cs': 'Computer Science (Universal)',
    'msc-dke': 'Internet- and Web-based Systems',
    'msc-itsec': 'IT-Security',
    'msc-vc': 'Visual Computing',
    'roles-assigned': 'You have been assigned the appropriate roles. Have fun!'
}


class I18n:
    def __init__(self, database: Database):
        self._database = database

    def get_text(self, discord_username: str, id: str, **kwargs):
        if id in TEXT_UNIVERSAL:
            return TEXT_UNIVERSAL[id]

        user_info = self._database.get_user_info(discord_username)
        language = user_info.language
        if language is None:
            raise Exception(f'A non-universal text {id=} was requested, but the user {discord_username=} does not have a specified language!')
        return self._get_text(language, id, **kwargs)

    def _get_text(self, language: UserLanguage, id: str, **kwargs):
        if id in TEXT_UNIVERSAL:
            return TEXT_UNIVERSAL[id]
        if id in TEXT_SPECIAL:
            return self._handle_special_text(language, id, **kwargs)
        if language == UserLanguage.GERMAN and id in TEXT_GERMAN:
            return TEXT_GERMAN[id]
        if language == UserLanguage.ENGLISH and id in TEXT_ENGLISH:
            return TEXT_ENGLISH[id]
        raise Exception(f'Cannot find translated text {id=} for language {language=}!')

    def _handle_special_text(self, language: UserLanguage, id: str, **kwargs):
        if id == ORDER_FOUND_CONFIRM:
            text = self._get_text(language, 'order-found-confirm-head') + ' '
            product = kwargs['product']
            programs = kwargs['programs']
            if product == Products.BACHELOR:
                if Programs.BACHELOR_OF_SCIENCE in programs:
                    text += self._get_text(language, 'order-found-confirm-bsc')
                if Programs.BACHELOR_OF_EDUCATION in programs:
                    text += self._get_text(language, 'order-found-confirm-bed')
                if Programs.JOINT_BACHELOR_OF_ARTS in programs:
                    text += self._get_text(language, 'order-found-confirm-jba')
                if Programs.TEACHING_AT_SECONDARY_SCHOOLS in programs:
                    text += self._get_text(language, 'order-found-confirm-lag')
            elif product == Products.MASTER:
                text += self._get_text(language, 'order-found-confirm-msc')
                for program in programs:
                    text += '\n  * '
                    if program == Programs.AUTONOMOUS_SYSTEMS:
                        text += self._get_text(language, 'msc-as')
                    elif program == Programs.DISTRIBUTED_SOFTWARE_SYSTEMS:
                        text += self._get_text(language, 'msc-dss')
                    elif program == Programs.UNIVERSAL:
                        text += self._get_text(language, 'msc-cs')
                    elif program == Programs.INTERNET_AND_WEBBASED_SYSTEMS:
                        text += self._get_text(language, 'msc-dke')
                    elif program == Programs.IT_SECURITY:
                        text += self._get_text(language, 'msc-itsec')
                    elif program == Programs.VISUAL_COMPUTING:
                        text += self._get_text(language, 'msc-vc')
            else:
                raise Exception(f'Unknown {product=}!')
        else:
            raise Exception(f'Unknown special text {id=}!')
        return text
