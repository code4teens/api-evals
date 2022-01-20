from flask import Flask

from api_evals import api_evals
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_evals)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
