from flask import Blueprint, jsonify, request

from database import db_session
from models import Cohort, Eval, User
from schemata import EvalSchema

api_evals = Blueprint('api_evals', __name__)


@api_evals.route('/evals')
def get_evals():
    evals = Eval.query.order_by(Eval.id).all()
    data = EvalSchema(many=True).dump(evals)

    return jsonify(data), 200


@api_evals.route('/evals', methods=['POST'])
def create_eval():
    keys = ['evaluator_id', 'evaluatee_id', 'cohort_id', 'date']

    if sorted([key for key in request.json]) == sorted(keys):
        evaluator_id = request.json.get('evaluator_id')
        evaluatee_id = request.json.get('evaluatee_id')
        cohort_id = request.json.get('cohort_id')
        date = request.json.get('date')
        evaluator = User.query.filter_by(id=evaluator_id).one_or_none()
        evaluatee = User.query.filter_by(id=evaluatee_id).one_or_none()
        cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

        if evaluator is not None and evaluatee is not None \
                and cohort is not None:
            existing_eval = Eval.query.filter_by(evaluator_id=evaluator_id)\
                .filter_by(evaluatee_id=evaluatee_id)\
                .filter_by(cohort_id=cohort_id)\
                .filter_by(date=date)\
                .one_or_none()

            if existing_eval is None:
                eval_schema = EvalSchema()

                try:
                    eval = eval_schema.load(request.json)
                except Exception as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    db_session.add(eval)
                    db_session.commit()
                    data = {
                        'title': 'Created',
                        'status': 201,
                        'detail': f'Eval {eval.id} created'
                    }

                    return data, 201
            else:
                data = {
                    'title': 'Conflict',
                    'status': 409,
                    'detail': 'Eval with posted details already exists'
                }

                return data, 409
        else:
            data = {
                'title': 'Bad Request',
                'status': 400,
                'detail': 'Evaluator, evaluatee or cohort does not exist'
            }

            return data, 400

    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400


@api_evals.route('/evals/<int:id>')
def get_eval(id):
    eval = Eval.query.filter_by(id=id).one_or_none()

    if eval is not None:
        data = EvalSchema().dump(eval)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Eval {id} not found'
        }

        return data, 404


@api_evals.route('/evals/<int:id>', methods=['PUT'])
def update_eval(id):
    keys = [
        'evaluator_id',
        'evaluatee_id',
        'cohort_id',
        'date',
        'review',
        'feedback'
    ]

    if all(key in keys for key in request.json):
        existing_eval = Eval.query.filter_by(id=id).one_or_none()

        if existing_eval is not None:
            eval_schema = EvalSchema()

            try:
                eval = eval_schema.load(request.json)
            except Exception as _:
                data = {
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'Some values failed validation'
                }

                return data, 400
            else:
                eval.id = existing_eval.id
                db_session.merge(eval)
                db_session.commit()
                data = eval_schema.dump(existing_eval)

                return data, 200
        else:
            data = {
                'title': 'Not Found',
                'status': 404,
                'detail': f'Eval {id} not found'
            }

            return data, 404
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400
