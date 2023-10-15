# matcha.py
import os
from matcha import create_app
from matcha import db

app = create_app(os.environ.get('FLASK_ENV') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=None)
