# matcha/model/CompetenceHardSkill.py
from datetime import datetime

from .. import db


class CompetenceHardSkill(db.Model):
    __bind_key__ = "learning_path"
    __tablename__ = 'competence_hard_skills'

    id = db.Column(db.Integer, primary_key=True)
    code_competence = db.Column(db.String(45))
    code_skill =  db.Column(db.String(45))

    def __repr__(self):
        return f'<CompetenceHardSkill {self.code_competence!r}>'

    def to_json(self):
        json_competence_hard_skill = {
            'id': self.id,
            'code_competence': self.code_competence,
            'code_skill': self.code_skill
        }
        return json_competence_hard_skill
