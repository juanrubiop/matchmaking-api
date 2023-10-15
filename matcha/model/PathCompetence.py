# matcha/model/PathCompetence.py
from datetime import datetime

from .. import db


class PathCompetence(db.Model):
    __bind_key__ = "learning_path"
    __tablename__ = 'path_competence'

    id = db.Column(db.Integer, primary_key=True)
    code_path = db.Column(db.String(45))
    code_competence = db.Column(db.String(45))


    def __repr__(self):
        return f'<PathCompetence {self.code_path!r}>'

    def to_json(self):
        json_path_competence = {
            'id': self.id,
            'code_path': self.code_path,
            'code_competence': self.code_competence
        }
        return json_path_competence
