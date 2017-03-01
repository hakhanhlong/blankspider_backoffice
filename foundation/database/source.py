from app import db
from datetime import datetime

class SOURCES(db.Document):
    name = db.StringField(max_length=255, required=True)
    mode = db.StringField(max_length=10, required=True)
    is_active = db.BooleanField(default=False)
    status = db.StringField(max_length=20, required=True)
    created_date = db.DateTimeField(default=datetime.now, required=True)
    created_by = db.StringField(max_length=255, required=True)
    project_id = db.StringField(max_length=255, required=True)
    project_name = db.StringField(max_length=255, required=True)
    type_spider = db.StringField(max_length=255, required=True, default=u'DEFAULT')

