import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'test.db')

AUTHENTICATION_BACKEND = 'ldapauthenticationbackend.LDAPAuthenticationBackend'
BACKEND_PATH = 'sqlite:///{}'.format(DB_PATH)
#BACKEND_PATH = 'mysql://eliakimdjango:mnk21jie1892ud9@eliakimdjango.mysql.pythonanywhere-services.com/eliakimdjango$default'
