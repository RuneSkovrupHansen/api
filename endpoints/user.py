import functools

from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

"""It is common for a resource, such as a user, to have two endpoints.
One endpoint to modify a single entry, and one entry to modify
multiple entries at once. For example:

/user/<id>
/user

The flask_restful refers to the endpoint used to modify multiple
entries at once as a list.

The endpoints would support the following methods:

/user/<id>
    GET
    DELETE
    PUT

/user
    GET
    DELETE
    PUT
    POST

Note that /user/<id> cannot support the POST method, since POST is used
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


def get_next_id():
    return int(user_list[-1]["id"])+1


def get_id_index(id):
    for index, user in enumerate(user_list):
        if int(user["id"]) == id:
            return index
    return -1


"""Decorator which aborts if passed schema cannot be validated.

The decorator aborts with error code 400 and returns the errors.

Since the schema must be passed to the decorator, the function
is actually creating a decorator, which then creates a wrapper.

https://stackoverflow.com/a/5929165/13308972
"""


def schema_validator(schema):
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
    if get_id_index(value) == -1:
        raise ValidationError(
            "A user with the specified id does not exist.")


"""Since a schema cannot be used to validate the
user id when it is specified as part of the url,
we create a decorator which aborts if id does not
exist."""


def abort_on_invalid_id(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if get_id_index(kwargs.get("id")) == -1:
            abort(400, message="A user with the specified id does not exist.")
        return func(*args, **kwargs)
    return wrapper


class User(Resource):

    @abort_on_invalid_id
    def get(self, id):
        return user_list[get_id_index(id)]

    @abort_on_invalid_id
    def delete(self, id):
        global user_list
        user_list.pop(get_id_index(id))

    @abort_on_invalid_id
    def put(self, id):
        global user_list
        index = get_id_index(id)
        user = user_list[index]

        for key, value in request.json.items():
            user[key] = value

        user_list[index] = user
        return user


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

    @ validates_schema
    def one_or_more(self, data, **kwargs):
        if "name" not in data and "age" not in data:
            raise ValidationError("No data passed")


# Strict mode is by default enabled to reject any other fields
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

    @ schema_validator(_get_delete_schema)
    def get(self):

        response = []
        for item in request.json:
            user = next(user for user in user_list if user["id"] == item["id"])
            response.append(user)

        return response

    @ schema_validator(_get_delete_schema)
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

    @ schema_validator(_put_schema)
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

    # Valid curl command
    # curl -X POST 127.0.0.1:5000/user -d '[{"name": "Rune", "age": "29"}, {"name": "Maria", "age": "27"}]' -H 'Content-Type: application/json'

    @ schema_validator(_post_schema)
    def post(self):

        global user_list

        response = []
        for item in request.json:

            user = {}
            user["id"] = get_next_id()

            # Add all values passed to user
            for key in item.keys():
                user[key] = item[key]

            user_list.append(user)
            response.append(user)

        return response
