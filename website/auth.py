from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_admin import AdminIndexView

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.user_home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

# @auth.route('/admin-login', methods=['GET','POST'])
# def admin_login():
#     if request.method == 'POST':
#         admin_key=request.form.get('admin_key')
#         password=request.form.get('password')
#         admin = Admin.query.filter_by(admin_key=admin_key).first()
#         if admin:
#             if admin.password==password:
#                 flash('Logged in as an admin!!', category='success')
#                 login_user(admin)
#                 AdminIndexView.index(AdminIndexView())
#             else:
#                 flash('Incorrect Password', category='error')
#         else:
#             flash('Admin key does not exist', category='error')
#     return render_template("admin/admin-login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.user_home'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email=request.form.get('email')
        fullName=request.form.get('fullName')
        password=request.form.get('password')
        passwordConfirm=request.form.get('passwordConfirm')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(fullName)<2: 
            flash('Name too short!', category='error')
        elif len(password)<4:
            flash("Password too short!", category='error')
        elif password!=passwordConfirm:
            flash('Password does not match!', category='error')
            pass
        else:
            #add user to database
            user = User(email=email, fullName=fullName, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.user_home'))
        
    return render_template("signup.html", user=current_user)
