from marshmallow import fields, Schema


class EvalSchema(Schema):
    id = fields.Integer(dump_only=True)
    evaluator_id = fields.Integer(load_only=True)
    evaluatee_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)
    date = fields.Date()
    review = fields.Dict(allow_none=True)
    feedback = fields.Dict(allow_none=True)

    evaluator = fields.Nested('UserSchema', dump_only=True)
    evaluatee = fields.Nested('UserSchema', dump_only=True)
    cohort = fields.Nested('CohortSchema', dump_only=True)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class CohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()
