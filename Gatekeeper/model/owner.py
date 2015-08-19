from Gatekeeper import app
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

class Owner(Resource):
    pass

class Owners(Resource):
    pass
