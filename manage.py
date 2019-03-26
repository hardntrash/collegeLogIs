from LogApp.app import app
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run(port='80')