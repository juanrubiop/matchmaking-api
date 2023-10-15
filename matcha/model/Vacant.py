# matcha/model/Vacant.py
import enum
from datetime import datetime

from .. import db


class Vacant(db.Model):
    __tablename__ = 'vacant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    vacant_level = db.Column(db.String(255))
    company_id = db.Column(db.Integer)
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    working_time = db.Column(db.Text)
    vacant_type = db.Column(db.Text)
    max_salary = db.Column(db.Float)
    min_salary = db.Column(db.Float)
    area = db.Column(db.String(255))
    education = db.Column(db.String(255))
    experience = db.Column(db.Text)
    status = db.Column(db.Text)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())

    def __repr__(self):
        return f'<Vacant {self.name!r}>'

    def to_json(self):
        json_vacant = {
            'id': self.id,
            'name': self.name,
            'vacant_level': self.vacant_level,
            'company_id': self.company_id,
            'country': self.country,
            'state': self.state,
            'experience': self.experience,
            'education': self.education,
            'status': self.status
        }
        return json_vacant
