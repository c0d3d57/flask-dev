# from sql_connect import db
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from conf import app
# db = db

db = SQLAlchemy(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(120))
    fullname = db.Column(db.String(40))
    address = db.Column(db.String(100))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    phone = db.Column(db.String(40))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80))
    message = db.Column(db.Text)
    sent_date = db.Column(db.DateTime)

    def __init__(self, sender, message, sent_date=None):
        self.sender = sender
        self.message = message
        if sent_date is None:
            sent_date = datetime.utcnow()
        self.sent_date = sent_date