from flask_login import UserMixin
from ldap3 import Server, Connection, ALL
from auth.app import app

class User(UserMixin):

    user_database = {}

    def __init__(self, username, password):
        self.id = username
        self.password = password
        self.user_database[self.id] = self

    @staticmethod
    def try_login(username, password):
        try:
            server = Server(app.config['LDAP_PROVIDER_URL'], get_info=ALL)
            Connection(server, 'uid={0}, cn=users, cn=accounts, dc=demo1, dc=freeipa, dc=org'.format(username),
                       password, auto_bind=True)
            return True
        except:
            return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @classmethod
    def get(cls, id):
        return cls.user_database.get(id)


