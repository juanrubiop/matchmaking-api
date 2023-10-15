# matcha/model/VacantSkillRequirement.py
import enum
from datetime import datetime

from .. import db


class VacantSkillRequirement(db.Model):
    __tablename__ = 'vacant_skill_requirements'

    id = db.Column(db.Integer, primary_key=True)
    vacant_id = db.Column(db.Integer)
    skill_id = db.Column(db.String(64))
    yoe = db.Column(db.Text)
    profficiency = db.Column(db.Text)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())

    def __repr__(self):
        return f'<VacantSkillRequirement {self.skill_id!r}>'

    def to_json(self):
        json_vacant_skill_requirement = {
            'vacant_id': self.vacant_id,
            'skill_id': self.skill_id,
            'id': self.id
        }
        return json_vacant_skill_requirement
