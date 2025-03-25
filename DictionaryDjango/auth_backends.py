from ldap3 import Server, Connection, ALL, SUBTREE
from django.conf import settings
from .models import BelstatUser
import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger('special.view')

class ActiveDirectorySessionBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            # Подключение к AD для проверки учетных данных
            logger.debug('Connecting to LDAP server')
            logger.debug(f'username: {username}, password: {password}')
            logger.debug(f'server: {settings.AD_SERVER}')
            server = Server(settings.AD_SERVER, get_info=ALL)
            logger.debug(f" logging as {username}@{settings.AD_DOMAIN}")
            conn = Connection(
                server,
                user=f"{username}@{settings.AD_DOMAIN}",
                password=password,
                auto_bind=True
            )
            logger.info('походу залогинились')
            # Если аутентификация успешна
            search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'

            conn.search(search_base=f'dc={settings.AD_DOMAIN},dc=local', search_filter=search_filter, search_scope=SUBTREE,
                        attributes=['sAMAccountName', 'objectGUID', 'cn'])

            # conn.search(
            #     settings.AD_SEARCH_BASE,
            #     f"(sAMAccountName={username})",
            #     attributes=['givenName', 'sn', 'mail']
            # )
            logger.info(' ищем себя')
            if conn.entries:
                logger.info('нашли себя')
                # logger.debug(f'username: {username}, first_name: {conn.entries[0].givenName}, last_name: {conn.entries[0].sn}')
                entry = conn.entries[0]
                user_data = {
                    'username': username,
                    'guid': str(entry.objectGUID),
                    'LDAP_Name': str(entry.cn),
                    'is_authenticated': True
                }
                request.session['user'] = user_data
                return user_data
            else:
                logger.info('не нашли себя')

            return None

        except Exception as e:
            logger.error(f"AD Auth Error: {e}")
            print(f"AD Auth Error: {e}")
            return None

    def get_user(self, request, user_data):
        if 'user' in request.session:
            return request.session['user']
        return None