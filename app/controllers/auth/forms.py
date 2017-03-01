from wtforms import StringField, BooleanField, Form, PasswordField
from wtforms import validators

class LoginForm(Form):
    username = StringField(u'UserName', [validators.DataRequired()])
    password = PasswordField(u'Password', [validators.DataRequired()])
    remember = BooleanField(u'Remember?')
