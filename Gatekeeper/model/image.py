from Gatekeeper import app
from flask_restful import Resource
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask import request
from Gatekeeper.model.util import fields_from_request
from Gatekeeper.model.util import load_from_yaml
from Gatekeeper.model.namespaced_schema import NamespacedSchema

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

sizes = {
    'xsmall': {'x': 16, 'y': 16},
    'small': {'x': 24, 'y': 24},
    'medium': {'x': 32, 'y': 32},
    'large': {'x': 48, 'y': 48},
}


class Image(Resource):

    class ModelView(NamespacedSchema):
        size = ma.Str()
        mime_Type = ma.Str()
        file_name = ma.Str()
        file_size = ma.Int()
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'DELETE'},
        })

        class Meta():
            name = 'image'
            plural_name = 'images'


    def __init__(self):
        self.object_id = None
        self.size = None # constrained list
        self.mime_Type = None # free form
        self.file_name = None # free form
        self.file_size = None # free form

    def get(self, object_id):
        instance = self.load(object_id)
        if instance:
            schema = self.ModelView(only=fields_from_request(request))
            data, errors = schema.dump(instance)
            return errors if errors else data
        # TODO: return error object if nothing could be loaded

    def load(self, image_id):
        try:
            images = load_from_yaml('images.yaml', Image)
            return images[image_id]
        except IndexError:
            return None


class Images(Resource):

    @property
    def images(self):
        return load_from_yaml('images.yaml', Image).values()

    def get(self):
        schema = Image.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.images)
        return errors if errors else data

api.add_resource(Images, '/images/')
api.add_resource(Image, '/images/<int:object_id>/')
