# -*- coding:utf-8 -*-
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class ACCOUNTS(db.Document):

    username = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255, required=True)
    fullname = db.StringField(max_length=255)
    password_hash = db.StringField(max_length=255, required=True)
    createddate = db.DateTimeField(default=datetime.now, required=True)
    lastlogin = db.DateTimeField(default=datetime.now)
    is_active = db.BooleanField(default=False)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attributes')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


