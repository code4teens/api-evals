from flask import Blueprint, jsonify

from models import Eval
from schemata import EvalSchema

api_evals = Blueprint('api_evals', __name__)


@api_evals.route('/evals')
def get_evals():
    evals = Eval.query.order_by(Eval.id).all()
    data = EvalSchema(many=True).dump(evals)

    return jsonify(data), 200
