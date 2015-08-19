from Gatekeeper import app
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

class Image(Resource):
    pass

class Images(Resource):
    pass

api.add_resource(Images, '/images/<int:object_id>/', endpoint='images')
