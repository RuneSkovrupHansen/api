#!/usr/bin/python3

from flask import Flask
from flask_restful import Api

from endpoints.version import Version
from endpoints.math import circle, triangle
from endpoints import user
from endpoints import secret

# Documentation on flask_restful
# https://flask-restful.readthedocs.io/en/latest/index.html

app = Flask(__name__)
api = Api(app)

"""Arguments can be passed to the constructor using the
parameters 'resource_class_args' and 'resource_class_kwargs'.

https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Api.add_resource
"""

"""Note that all endpoints are added with /api/v1/, this is done
to reserve to option to change the api version at a later time.
Could also be used for debugging / deployment."""

api.add_resource(Version, "/api/v1/version",
                 resource_class_kwargs={"major_version": "1", "minor_version": "0"})

api.add_resource(circle.Circumference, "/api/v1/math/circle/circumference")
api.add_resource(circle.Radius, "/api/v1/math/circle/radius")
api.add_resource(triangle.Area, "/api/v1/math/triangle/area")

# <int:user_id> matches that part of the url to a variable
# which is passed to the resource
api.add_resource(user.User, "/api/v1/user/<int:id>")
api.add_resource(user.UserList, "/api/v1/user")

api.add_resource(secret.Basic, "/api/v1/secret/basic")
api.add_resource(secret.Token, "/api/v1/secret/token")


def main():
    # Specify host as "0.0.0.0" to run on all addresses
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
