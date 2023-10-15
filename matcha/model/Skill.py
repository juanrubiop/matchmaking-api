# matcha/model/Skill.py
from datetime import datetime

from .. import db


class Skill(db.Model):
    __tablename__ = 'skill'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    focus = db.Column(db.String(255))
    category =  db.Column(db.String(255))
    source =  db.Column(db.String(255))
    description =  db.Column(db.String(255))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())

    def __repr__(self):
        return f'<Skill {self.name!r}>'

    def to_json(self):
        json_skill = {
            'id': self.id,
            'name': self.name,
            'focus': self.focus,
            'source': self.source,
            'category': self.category,
            'description': self.description
        }
        return json_skill
