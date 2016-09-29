from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['LDAP_PROVIDER_URL'] = 'ldap://ipa.demo1.freeipa.org:389'
app.config['LDAP_PROTOCOL_VERSION'] = 3
app.secret_key = 'dsajifjwq98f9qw8f98qw9fqwfkjqwofjw9qf89qw'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from my_app.auth.views import auth
app.register_blueprint(auth)

if __name__=='__main__':
  app.run()
