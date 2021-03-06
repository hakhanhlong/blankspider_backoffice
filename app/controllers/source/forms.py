from wtforms import *
from wtforms.validators import DataRequired
from foundation.dataservice import project_impl

class SourceForm(Form):
    name = StringField(u'NAME', validators=[DataRequired()])

    mode = SelectField(u'MODE', choices=(
        (u'GETNEW', u'GET NEW'),
        (u'UPDATE', u'UPDATE'),
        (u'TEST', u'TEST')
    ))
    is_active = SelectField(u'ACTIVE', choices=(
        (u'ACTIVE', u'ACTIVE'),
        (u'DEACTIVE', u'DEACTIVE')
    ))

    status = SelectField(u'STATUS', choices=(
        (u'NEED_CONFIG', u'NEED CONFIG'),
        (u'RUNNING', u'RUNNING'),
        (u'STOPPED', u'STOPPED')
    ))

    type_spider = SelectField(u'TYPE SPIDER', choices=[
        (u'Default', u'DEFAULT'),
        (u'Archivied', u'ARCHIVIED'),
        (u'Customize', u'CUSTOMIZE')
    ])

    #project = SelectField(u'SELECT PROJECT', choices=[(str(p.id), p.name) for p in project_impl.get_all()])
    project = SelectField(u'SELECT PROJECT')

    server_ip = StringField(u'SERVER IP', default="0.0.0.0")

class ConfigGeneralForm(Form):
    base_url = StringField(u'BASE URL', validators=[DataRequired()])
    video_base_url = StringField(u'VIDEO BASE URL', default="http://#")
    thread_number = StringField(u'THREAD NUMBER FIND LINK', default='1', validators=[DataRequired()])
    thread_number_parsing = StringField(u'THREAD NUMBER PARSING', default='1', validators=[DataRequired()])
    thread_sleep = StringField(u'THREAD SLEEP', default='200', validators=[DataRequired()])
    update_sleep = StringField(u'UPDATE SLEEP', default='300000', validators=[DataRequired()])
    max_trying_count = StringField(u'MAX TRYING COUNT', default='100', validators=[DataRequired()])
    post_url = StringField(u'POST URL', default="http://0.0.0.0")

    video_post_url = StringField(u'VIDEO POST URL', default="http://0.0.0.0")

    chk_unique_css = BooleanField(u'Unique Stylesheet?', default=0)
    filter_pdf = StringField(u'FILTER PDF BY')
    remove_filter_pdf = StringField(u'REMOVE FILTER PDF BY')







