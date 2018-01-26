from flask import render_template
from app import app,db
from flask_script import Manager
# from app import create_app,db
# app = create_app()
from flask_migrate import MigrateCommand,Migrate
manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command('db',MigrateCommand)
if __name__ == '__main__':
    app.run(debug = True)



# @app.errorhandler (404)
# def page_not_found (e):
#     return render_template ('404.html'),404
#
#
# @app.errorhandler (500)
# def internal_server_error (e):
#     return render_template ('500.html'),500

