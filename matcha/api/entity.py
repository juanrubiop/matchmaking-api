# matcha/api/entity.py
from flask import abort
from flask import current_app
from flask import request
from flask import jsonify
from sqlalchemy import text
from sqlalchemy import bindparam
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import api
from .. import db
from ..model import Skill,HardSkill
from ..model import Vacant
from ..model import VacantSkillRequirement
from ..utils.az_form_recognizer import check_azure_credentials, analyze_custom_documents ,extract_skills_from_text, extract_skills_from_text_db
from ..utils.az_form_recognizer import extract_data_from_cv


with open('matcha/model/sql/vacant_to_learning_path_rank.sql') as file:
    sql_vacant_to_learning_path_rank = file.read()
    sql_vacant_to_learning_path_rank = text(sql_vacant_to_learning_path_rank)


@api.route('/skill/<id>', methods=['GET'])
def get_skill(id):
    s = Skill()
    s = s.query.filter_by(id=id).first_or_404()
    return s.to_json()


@api.route('/vacant/<int:id>', methods=['GET'])
def get_vacant(id):
    v = Vacant()
    v = v.query.filter_by(id=id).first_or_404()
    return v.to_json()


@api.route('/vacant-skill-requirements/<int:vacant_id>', methods=['GET'])
def get_vacant_skill_requirements(vacant_id):
    r = VacantSkillRequirement
    s = Skill
    q = db.session.execute(db.select(r.vacant_id, s.name.label('skill_name'))\
                             .join(r, r.skill_id == s.id)\
                             .filter_by(vacant_id=vacant_id)).all()
    if not q:
        abort(404, 'Vacant not found.')
    return {
        'vacant_id': vacant_id,
        'skill_names': [ row.skill_name for row in q ]
    }


@api.route('/vacant-learning-path-affinity', methods=['POST'])
def get_v_lp_affinity():
    req = request.get_json()
    skill_values = req['vacant_required_skills']

    engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['learning_path'])
    Session = sessionmaker(engine)
    sql = sql_vacant_to_learning_path_rank.bindparams(bindparam('values', expanding=True))
    with Session() as session:
        r = session.execute(sql, {'values': tuple(skill_values)}).fetchall()
    
    if not r:
        abort(404)
    l = []
    for row in r:
        matched_skill_names = [None] if row.matched_skills_names is None else row.matched_skills_names.split('$')
        matched_skill_codes = [None] if row.matched_skills_codes is None else row.matched_skills_codes.split('$')
        unmatched_skill_names = [None] if row.unmatched_skills_names is None else row.unmatched_skills_names.split('$')
        unmatched_skill_codes = [None] if row.unmatched_skills_codes is None else row.unmatched_skills_codes.split('$')
        l.append({
            'code_path': row.code_path,
            'affinity': row.affinity,
            'name_path': row.name_path,
            'n_skills': row.n_skills,
            'rank': row.rank,
            'matched_skills': [{'skill_name': n, 'skill_code': c} for n, c in zip(matched_skill_names, matched_skill_codes)],
            'unmatched_skills': [{'skill_name': n, 'skill_code': c} for n, c in zip(unmatched_skill_names, unmatched_skill_codes)],
        })
    if req['top_n'] is not None:
        l = l[:req['top_n'] if req['top_n'] < len(l) else len(l)]
    return l

@api.route('/parse-cv-skills', methods=['POST'])
def parse_cv_skills_az_recog():
    cv_filename = request.json.get('cv_filename')
    cv_base64_string = request.json.get('cv_in_bytes')
    credentials={
        'CUSTOM_BUILT_MODEL_ID':current_app.config['CUSTOM_BUILT_MODEL_ID'],
        'AZURE_FORM_RECOGNIZER_ENDPOINT':current_app.config['AZURE_FORM_RECOGNIZER_ENDPOINT'],
        'AZURE_FORM_RECOGNIZER_KEY':current_app.config['AZURE_FORM_RECOGNIZER_KEY'],
        'CONTAINER_SAS_URL':current_app.config['CONTAINER_SAS_URL']
    }

    if check_azure_credentials(credentials):
        result=analyze_custom_documents(credentials,cv_base64_string)
        hardskill=extract_skills_from_text(result)


    return jsonify({
        'cv_filename': cv_filename,
        'skills': hardskill
    })

@api.route('/parse-cv-skills-db', methods=['POST'])
def parse_cv_skills_az_recog_db():
    cv_filename = request.json.get('cv_filename')
    cv_base64_string = request.json.get('cv_in_bytes')
    credentials={
        'CUSTOM_BUILT_MODEL_ID':current_app.config['CUSTOM_BUILT_MODEL_ID'],
        'AZURE_FORM_RECOGNIZER_ENDPOINT':current_app.config['AZURE_FORM_RECOGNIZER_ENDPOINT'],
        'AZURE_FORM_RECOGNIZER_KEY':current_app.config['AZURE_FORM_RECOGNIZER_KEY'],
        'CONTAINER_SAS_URL':current_app.config['CONTAINER_SAS_URL']
    }

    s = HardSkill
    query = db.session.execute(db.select(s.name_hskill.label('skill_name'))).all()
    skill_list_db=[row.skill_name for row in query ]
    if check_azure_credentials(credentials):
        result=analyze_custom_documents(credentials,cv_base64_string)
        hardskills=extract_skills_from_text_db(result,skill_list_db)

    return jsonify({
        'cv_filename': cv_filename,
        'skills':  hardskills
    })

@api.route('/extract-personal-info', methods=['POST'])
def extract_skills_from_cv():
    cv_filename = request.json.get('cv_filename')
    cv_base64_string = request.json.get('cv_in_bytes')
    credentials={
        'CUSTOM_BUILT_MODEL_ID':current_app.config['CUSTOM_BUILT_MODEL_ID'],
        'AZURE_FORM_RECOGNIZER_ENDPOINT':current_app.config['AZURE_FORM_RECOGNIZER_ENDPOINT'],
        'AZURE_FORM_RECOGNIZER_KEY':current_app.config['AZURE_FORM_RECOGNIZER_KEY'],
        'CONTAINER_SAS_URL':current_app.config['CONTAINER_SAS_URL']
    }
    if check_azure_credentials(credentials):
        result=analyze_custom_documents(credentials,cv_base64_string)
        user_info=extract_data_from_cv(result)
    user_info['cv_filename']=cv_filename
    print(type(user_info['names'][0]))
    
    return jsonify(user_info)
