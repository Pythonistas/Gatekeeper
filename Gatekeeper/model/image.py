from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
import yaml

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

sizes = {
    'xsmall': {'x': 16, 'y': 16},
    'small': {'x': 24, 'y': 24},
    'medium': {'x': 32, 'y': 32},
    'large': {'x': 48, 'y': 48},
}

# Is there a better way to share this code?
def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


class Image(Resource):

    class ModelView(ma.Schema):
        size = ma.Str()
        mime_Type = ma.Str()
        file_name = ma.Str()
        file_size = ma.Int()
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('image', object_id='<object_id>'), 'method': 'DELETE'},
        })

        @staticmethod
        def get_envelope_key(many):
            return 'images' if many else 'image'

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

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
            images = Images.load_from_yaml()
            return images[image_id]
        except IndexError:
            return None


class Images(Resource):

    @staticmethod
    def load_from_yaml():
        images = {}
        try:
            with open("images.yaml", 'r') as stream:
                for data in yaml.safe_load(stream):
                    cur_image = Image()
                    for key, value in data.items():
                        setattr(cur_image, key, value)
                    images[cur_image.object_id] = cur_image
        except OSError:
            return None
        return images

    @property
    def images(self):
        return Images.load_from_yaml().values()

    def get(self):
        schema = Image.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.images)
        return errors if errors else data

api.add_resource(Images, '/images/')
api.add_resource(Image, '/images/<int:object_id>/')
