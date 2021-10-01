from src.constants import PRETIX_ORGANIZER, PRETIX_EVENT
from src.pretix_api import PretixApi
from src.pretix_cache import PretixCache
from src.tokens import PRETIX_AUTH_TOKEN


def main():
    cache = PretixCache(PretixApi('https://anmeldung.d120.de', PRETIX_AUTH_TOKEN), PRETIX_ORGANIZER, PRETIX_EVENT)
    print('Refreshing pretix cache database...')
    cache.refresh()
    print('Finished!')


if __name__ == "__main__":
    main()
