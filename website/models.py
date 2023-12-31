from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullName = db.Column(db.String(150))
    # notes = db.relationship('Note')
    projects = db.relationship('Project')

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     data = db.Column(db.String(5000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now()) 
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.String(3000))
    csv_data = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_key =db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))




