from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

# IMPORTANT
# add path to website folder
UPLOAD_FOLDER = '/website/static/cv'


# allowed extension for file upload
ALLOWED_EXTENSIONS = {'pdf'}



def create_app():
    app = Flask(__name__)
    # change secret key
    app.config['SECRET_KEY'] = 'insert secret key here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# create database if it doesnt exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
