from flask_restful import Resource


class Version(Resource):

    """Serves a version string."""

    def __init__(self, version) -> None:
        self.version = version
        super().__init__()

    def get(self):
        return self.version
