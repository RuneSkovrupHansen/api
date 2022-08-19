import functools
import re

from flask import request
from flask_restful import Resource, abort

SECRET = "No one expects the spanish inquisition!"

valid_tokens = [
    "qlv3onxe59",
    "0ib5ym8t4o",
    "fgqa8fepmq"
]

user_credentials = {
    "john_doe": "123456",
    "jane_doe": "1q2w3e",
    "steve": "qwerty"
}


# Expect "Authorization": "Basic <username>:<password>"
def basic_authentication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        authorization = request.headers.get("Authorization", None)
        if authorization is None:
            abort(401)

        split = authorization.strip().split(" ")
        if len(split) != 2:
            abort(401)

        if split[0].strip().lower() != 'basic':
            abort(401)

        try:
            username, password = split[1].split(':', 1)
        except:
            abort(401)

        if username not in user_credentials:
            print(user_credentials)
            abort(401)

        if password != user_credentials[username]:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def token_authentication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        token = request.headers.get("X-Api-Token", None)
        if token not in valid_tokens:
            print(token)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


"""Setting the method_decorator attribute without
specifying a method will apply the decorator to all
methods of all inherited resources."""


class BasicAuthResource(Resource):
    method_decorators = [basic_authentication]


class TokenAuthResource(Resource):
    method_decorators = [token_authentication]


# Valid curl command
# curl -X GET 127.0.0.1:5000/api/v1/secret/basic -H 'Authorization: Basic steve:qwerty'

class Basic(BasicAuthResource):

    def get(self):
        return SECRET

# Valid curl command
# curl -X GET 127.0.0.1:5000/api/v1/secret/token -H 'X-Api-Token: qlv3onxe59'


class Token(TokenAuthResource):

    def get(self):
        return SECRET
