from flask import request
from flask_restful import Resource


class Version(Resource):
    """Serves a version string."""

    def __init__(self, major_version, minor_version) -> None:
        self.major_version = major_version
        self.minor_version = minor_version
        super().__init__()

    # curl -X GET 127.0.0.1:5000/api/v1/version -H 'X-Api-Token: qlv3onxe59'

    def get(self):
        request_version = request.headers.get("Version", None)

        if request_version == "1":
            version = ".".join([self.major_version, self.minor_version])
        else:  # Default to newest version
            version = {"major_version": self.major_version,
                       "minor_version": self.minor_version}

        return version
