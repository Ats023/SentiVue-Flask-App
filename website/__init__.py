from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
#create database
db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         if not current_user.is_authenticated:
#             return redirect(url_for('.login'))
#         return super(MyAdminIndexView,self).index()

#     @expose('/admin-login/', methods=['GET', 'POST'])
#     def login(self):
#         if request.method == 'POST':
#             admin_key = request.form.get('admin_key')
#             password = request.form.get('password')
            
#             # Check if the entered admin key and password are correct
#             admin = Admin.query.filter_by(admin_key=admin_key, password=password).first()
#             if admin:
#                 login_user(admin)
#                 return redirect(url_for('.index'))
            
#         return self.render('admin/admin-login.html',user=current_user)
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
    with app.app_context():
        db.create_all()
    from .models import User,Admin,Project
    from flask_admin.base import MenuLink, MenuView
    from flask_admin import Admin, AdminIndexView, BaseView, expose
    class MyAdminIndexView(AdminIndexView):
        def is_visible(self):
            return False
        @expose('/')
        def index(self):
            if not current_user.is_authenticated:
                return redirect(url_for('.login'))
            return super(MyAdminIndexView,self).index()

        @expose('/admin-login/', methods=['GET', 'POST'])
        def login(self):
            if request.method == 'POST':
                admin_key = request.form.get('admin_key')
                password = request.form.get('password')
                
                # Check if the entered admin key and password are correct
                admin = models.Admin.query.filter_by(admin_key=admin_key, password=password).first()
                if admin:
                    login_user(admin)
                    return redirect(url_for('.index'))
                else:
                    flash("Incorrect Details! Unauthorized to access admin portal", category="error")
                
            return redirect(url_for('views.user_home'))
    admin = Admin(index_view=MyAdminIndexView())
    admin.init_app(app)
    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

    class UserView(ModelView):
        create_modal = True
        can_view_details = True
        can_edit = True
        column_exclude_list=['password',]
        column_list = ['email', 'fullName', 'project_count']
        def project_count_formatter(view, context, model, name):
            return len(model.projects)

        column_formatters = {
            'project_count': project_count_formatter
        }
        
    admin.add_view(UserView(User,db.session))
    admin.add_link(MenuLink(name='logout', url='/logout'))
    login_manager = LoginManager()
    
    #where user should be directed to if they are not logged in
    login_manager.login_view = 'views.user_home' 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
