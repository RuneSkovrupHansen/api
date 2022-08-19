from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields


class AreaGetSchema(Schema):
    """Schema for GET method of area resource."""
    height = fields.Float(required=True)
    base = fields.Float(required=True)


class Area(Resource):
    """Endpoint to calculate area of triangle based on height and base."""

    _get_schema = AreaGetSchema()

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        # .get_json() must be used for json requests
        request_json = request.get_json()
        errors = self._get_schema.validate(request_json)
        if errors:
            abort(400, message=str(errors))

        height = float(request_json["height"])
        base = float(request_json["base"])
        return height*base/2
