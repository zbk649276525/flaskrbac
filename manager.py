from flask import render_template
from flask_script import Manager
from app import create_app,db
from flask_migrate import MigrateCommand,Migrate
app = create_app()
manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command('db',MigrateCommand)



# @app.errorhandler (404)
# def page_not_found (e):
#     return render_template ('404.html'),404
#
#
# @app.errorhandler (500)
# def internal_server_error (e):
#     return render_template ('500.html'),500
if __name__ == '__main__':
    app.run()
