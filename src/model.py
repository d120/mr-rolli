import enum
from typing import List, Optional



class Products(enum.Enum):
    BACHELOR = 0
    MASTER = 1



class Programs(enum.Enum):
    # Bachelor.
    BACHELOR_OF_SCIENCE = 0
    BACHELOR_OF_EDUCATION = 1
    JOINT_BACHELOR_OF_ARTS = 2
    TEACHING_AT_SECONDARY_SCHOOLS = 3
    # Master.
    AUTONOMOUS_SYSTEMS = 4
    DISTRIBUTED_SOFTWARE_SYSTEMS = 5
    UNIVERSAL = 6
    INTERNET_AND_WEBBASED_SYSTEMS = 7
    IT_SECURITY = 8
    VISUAL_COMPUTING = 9



class UserState(enum.Enum):
    NEW = 0
    LANGUAGE_REQUESTED = 1
    LANGUAGE_CONFIGURED = 2


    def next(user_state: 'UserState') -> 'UserState':
        return UserState(user_state.value + 1)



class UserLanguage(enum.Enum):
    ENGLISH = 0
    GERMAN = 1



class UserInfo:
    state: UserState
    language: UserLanguage


    def __init__(self, state: UserState, language: UserLanguage):
        self.state = state
        self.language = language


    def next_state(self):
        self.state = self.state.next()
        return self



class Order:
    discord_username: str
    product: Products
    programs: List[Programs]
    programming_course: Optional[bool]


    def __init__(self, discord_username: str, product: Products, programs: List[Programs], programming_course: Optional[bool]):
        self.discord_username = discord_username
        self.product = product
        self.programs = programs
        self.programming_course = programming_course
