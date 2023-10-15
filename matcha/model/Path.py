# matcha/model/Path.py
from datetime import datetime

from .. import db


class Path(db.Model):
    __bind_key__ = "learning_path"
    __tablename__ = 'path'

    code_path = db.Column(db.String(50), primary_key=True)
    name_path = db.Column(db.String(80))
    type_path = db.Column(db.String(45))
    active = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())

    def __repr__(self):
        return f'<Path {self.name_path!r}>'

    def to_json(self):
        json_path = {
            'code_path': self.code_path,
            'name': self.name_path,
            'type_path': self.type_path,
            'is_active': self.active
        }
        return json_path
