from flask import Flask
from flask_login import LoginManager

emile_server = Flask(__name__)
emile_server.config['LDAP_PROVIDER_URL'] = 'ldap://ipa.demo1.freeipa.org:389'
emile_server.config['LDAP_PROTOCOL_VERSION'] = 3
emile_server.secret_key = 'dsajifjwq98f9qw8f98qw9fqwfkjqwofjw9qf89qw'

login_manager = LoginManager()
login_manager.init_app(emile_server)
login_manager.login_view = 'auth.login'

from . import views
emile_server.register_blueprint(views.auth)