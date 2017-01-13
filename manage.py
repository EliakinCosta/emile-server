from flask_migrate import Manager, Migrate, MigrateCommand
from emile_server import app
from backend import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
