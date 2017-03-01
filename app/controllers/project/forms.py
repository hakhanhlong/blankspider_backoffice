from wtforms import *
from wtforms.validators import DataRequired


class AddForm(Form):
    name = StringField(u'Project Name', validators=[DataRequired()])

class EditForm(Form):
    name = StringField(u'Project Name', validators=[DataRequired()])
