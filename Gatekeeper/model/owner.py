from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
import yaml

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

# Is there a better way to share this code?
def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


class Owner(Resource):

    class ModelView(ma.Schema):
        first_name = ma.Str()
        last_name = ma.Str()
        phone_number = ma.Str() # TODO: Define a better schema for phone number formatting/validation, etc.
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'DELETE'},
        })

        @staticmethod
        def get_envelope_key(many):
            return 'owners' if many else 'owner'

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}
    
    def __init__(self):
        self.object_id = None
        self.first_name = None # free form
        self.last_name = None # free form
        self.phone_number = None # free form

    def get(self, object_id):
        instance = self.load(object_id)
        if instance:
            schema = self.ModelView(only=fields_from_request(request))
            data, errors = schema.dump(instance)
            return errors if errors else data
        # TODO: return error object if nothing could be loaded

    def load(self, owner_id):
        try:
            owners = Owners.load_from_yaml()
            return owners[owner_id]
        except IndexError:
            return None


class Owners(Resource):

    @staticmethod
    def load_from_yaml():
        owners = {}
        try:
            with open("owners.yaml", 'r') as stream:
                for data in yaml.safe_load(stream):
                    cur_owner = Owner()
                    for key, value in data.items():
                        setattr(cur_owner, key, value)
                    owners[cur_owner.object_id] = cur_owner
        except OSError:
            return None
        return owners

    @property
    def owners(self):
        return Owners.load_from_yaml().values()

    def get(self):
        schema = Owner.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.owners)
        return errors if errors else data

api.add_resource(Owners, '/owners/')
api.add_resource(Owner, '/owners/<int:object_id>')
