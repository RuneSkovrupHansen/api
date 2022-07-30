import functools

from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

"""It is common for a resource, such as a user, to have two endpoints.
One endpoint to modify a single entry, and one entry to modify
multiple entries at once. For example:

/user/<user_id>
/user

The flask_restful refers to the endpoint used to modify multiple
entries at once as a list.

The endpoints would support the following methods:

/user/<user_id>
    GET
    DELETE
    PUT
    
/user
    GET
    DELETE
    PUT
    POST
    
Note that /user/<user_id> cannot support the POST method, since POST is used
to add a new value and the endpoint already has an id.
"""

"""Validation

Use built-in validation methods
https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#api-validators

Schema-level validation used to validate the relation between data
https://marshmallow.readthedocs.io/en/stable/extending.html#schema-level-validation
"""

# Mock data
user_list = [
    {"id": "0", "name": "John", "age": "30"},
    {"id": "1", "name": "Steve", "age": "41"},
    {"id": "2", "name": "Bob", "age": "34"}
]

"""Decorator which aborts if passed schema cannot be validated.

The decorator aborts with error code 400 and returns the errors.

Since the schema must be passed to the decorator, the function
is actually creating a decorator, which then creates a wrapper.

https://stackoverflow.com/a/5929165/13308972
"""


def abort_validator(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            errors = schema.validate(request.json)
            if errors:
                abort(400, message=str(errors))
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_id_exists(value):
    """Check that an id exists."""
    for user in user_list:
        if int(user["id"]) == value:
            return
    raise ValidationError("A user with the specified id does not exist.")


class User(Resource):

    def get(self, user_id):
        pass

    def delete(self, user_id):
        pass

    def put(self, user_id):
        pass


class UserListGetDeleteSchema(Schema):
    id = fields.Integer(validate=validate_id_exists, required=True)


class UserListPutSchema(Schema):

    id = fields.Integer(validate=validate_id_exists, required=True)

    def validate_no_spaces(value):
        if " " in value:
            raise ValidationError(f"The specified name contains a space.")

    # Use custom validation method
    name = fields.String(validate=validate_no_spaces)
    age = fields.Integer(validate=validate.Range(min=0, max=100))

    @validates_schema
    def one_or_more(self, data, **kwargs):
        if "name" not in data and "age" not in data:
            raise ValidationError("No data passed")


class UserListPostSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)


class UserList(Resource):

    # Since the endpoint must handle one or more users we set
    # many=True for all schemas.
    _get_delete_schema = UserListGetDeleteSchema(many=True)
    _put_schema = UserListPutSchema(many=True)
    _post_schema = UserListPostSchema(many=True)

    # curl command to call endpoint method
    # curl -X GET 127.0.0.1:5000/user -d '[{"id": "0"}, {"id": "1"}]' -H 'Content-Type: application/json'

    @abort_validator(_get_delete_schema)
    def get(self):
        print(request.json)
        pass

    @abort_validator(_get_delete_schema)
    def delete(self):

        global user_list

        id_list = []
        for item in request.json:
            id_list.append(item["id"])

        new_list = [user for user in user_list if user["id"] not in id_list]
        user_list = new_list

    # curl command to trigger name validator error
    # curl -X PUT 127.0.0.1:5000/user -d '[{"id": "0", "name": "Rune Hansen"}, {"id": "1"}]' -H 'Content-Type: application/json'

    # valid curl command
    # curl -X PUT 127.0.0.1:5000/user -d '[{"id": "0", "name": "Rune"}, {"id": "1", "age": "29"}]' -H 'Content-Type: application/json'

    @abort_validator(_put_schema)
    def put(self):

        global user_list

        response = []
        for item in request.json:

            id = item["id"]
            del item["id"]

            # Get user and corresponding index from user_list
            index, user = next((index, user) for (index, user) in enumerate(
                user_list) if user["id"] == id)

            for key in item.keys():
                user[key] = item[key]

            user_list[index] = user
            response.append(user)

        return response

    @abort_validator(_post_schema)
    def post(self):
        print(request.json)
        pass
