from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager
#create database
db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

#Create a flask app with a secret key to encrypt files
def create_app():
    app = Flask(__name__)
    app.secret_key = 'ghtcleg'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    migrate.init_app(app, db)
    app.db = db;
    #register the views
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    from .models import User,Note,Project
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    
    #where user should be directed to if they are not logged in
    login_manager.login_view = 'views.user_home' 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
