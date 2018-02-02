from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from app import create_app,db

app = create_app ()

manage = Manager (app)
migrate = Migrate (app,db)
manage.add_command ('db',MigrateCommand)
if __name__ == '__main__':
    app.run (debug = True)
    # manage.run ()


