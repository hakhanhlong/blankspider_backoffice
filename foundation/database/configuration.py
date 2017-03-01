from app import db
from datetime import datetime

class CONFIGURATIONS(db.Document):
    system_object = db.StringField(max_length=255, required=True)
    system_object_id = db.StringField(max_length=255, required=True)
    created_date = db.DateTimeField(default=datetime.now)
    config = db.DictField()