from emile_server import app
import importlib
from flask import request
import settings


@app.route('/login', methods=['POST'])
def login():
    module_name, class_name = settings.AUTHENTICATION_BACKEND.rsplit('.', maxsplit=1)
    m = importlib.import_module(module_name)
    cls = getattr(m, class_name)

    email = request.form.get('email')
    password = request.form.get('password')

    return cls().authenticate(email, password)