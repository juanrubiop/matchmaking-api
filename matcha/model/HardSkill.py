# matcha/model/HardSkill.py
from datetime import datetime

from .. import db


class HardSkill(db.Model):
    __bind_key__ = "learning_path"
    __tablename__ = 'hard_skills'
    
    code_hskill = db.Column(db.Integer, primary_key=True)
    name_hskill = db.Column(db.String(45))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<HardSkill {self.code_hskill!r}>'

    def to_json(self):
        json_hard_skill = {
            'code_hard_skill': self.code_hskill,
            'name': self.name_hskill
        }
        return json_hard_skill
