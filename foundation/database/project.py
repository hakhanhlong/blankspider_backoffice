from app import db
from datetime import datetime


class PROJECTS(db.Document):
    name = db.StringField(max_length=255, required=True)
    created_by = db.StringField(max_length=255, required=True)
    created_date = db.DateTimeField(default=datetime.now, required=True)
    source_count = db.IntField(default=0, required=True)
