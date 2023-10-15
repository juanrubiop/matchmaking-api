# matcha/api/__init__.py
from . import api


@api.route('/', methods=['GET'])
def index():
    return '<h1>Server is running.</h1>'


@api.route('/status', methods=['GET'])
def hello():
    return '<h1>Server is running.</h1>'


@api.route('/about', methods=['GET'])
def about():
    return 'Match-making ranking app. Use HTTP Basic Auth or JSON Web Token.'
