import uuid
import marshmallow
from marshmallow import validate, fields


def gen_uuid():
    return str(uuid.uuid4()).replace("-", "")


class BaseSchema(marshmallow.Schema):
    class Meta:
        strict = True
        ordered = True


class FooBodySchema(BaseSchema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=512))
    email = fields.String(required=True, validate=validate.Email())
    some_id = fields.String(missing=gen_uuid, validate=validate.Length(min=1, max=256))
    some_state = fields.Dict(missing=lambda: {})


class BarBodySchema(BaseSchema):
    a_field = fields.String(required=True, validate=validate.Length(min=1, max=512))
    b_field = fields.String(required=True, validate=validate.Length(min=1, max=512))
