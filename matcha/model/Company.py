# matcha/model/Company.py
from datetime import datetime

from .. import db


class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    logo =  db.Column(db.String(255))
    campus =  db.Column(db.String(255))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())

    def __repr__(self):
        return f'<Company {self.name!r}>'

    def to_json(self):
        json_company = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return json_company
