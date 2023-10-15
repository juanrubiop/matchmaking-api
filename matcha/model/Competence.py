# matcha/model/Competence.py
from datetime import datetime

from .. import db


class Competence(db.Model):
    __bind_key__ = "learning_path"
    __tablename__ = 'competences'
    
    code_competence = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(150))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime())


    def __repr__(self):
        return f'<Competence {self.code_competence!r}>'

    def to_json(self):
        json_competence = {
            'id': self.code_competence,
            'description': self.description
        }
        return json_competence
