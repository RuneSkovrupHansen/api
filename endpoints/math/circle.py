import math

from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields

"""Module containing endpoints related to circle math.

Use of the marshmallow library for parsing request data.

Documentation: https://marshmallow.readthedocs.io/en/stable/
Example: https://stackoverflow.com/a/30779996/13308972
"""


class CircumferenceGetSchema(Schema):
    """Schema for GET method of circumference resource."""
    radius = fields.Float(required=True)


class Circumference(Resource):

    """Endpoint to calculate circumference of a circle based on radius."""

    _get_schema = CircumferenceGetSchema()

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        # .get_json() must be used for json requests
        request_json = request.get_json()
        errors = self._get_schema.validate(request_json)
        if errors:
            abort(400, message=str(errors))

        radius = float(request_json["radius"])
        return radius*2*math.pi


class RadiusGetSchema(Schema):
    """Schema for GET method of radius resource."""
    circumference = fields.Float(required=True)


class Radius(Resource):

    """Endpoint to calculate radius of a circle based on radius."""

    _get_schema = RadiusGetSchema()

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        # .get_json() must be used for json requests
        request_json = request.get_json()
        errors = self._get_schema.validate(request_json)
        if errors:
            abort(400, message=str(errors))

        circumference = float(request_json["circumference"])
        return circumference/(2*math.pi)
