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


class Owner(Resource):

    class ModelView(NamespacedSchema):
        first_name = ma.Str()
        last_name = ma.Str()
        phone_number = ma.Str() # TODO: Define a better schema for phone number formatting/validation, etc.
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('owner', object_id='<object_id>'), 'method': 'DELETE'},
        })

        class Meta:
            name = 'owner'
            plural_name = 'owners'


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
            owners = load_from_yaml("owners.yaml", Owner)
            return owners[owner_id]
        except IndexError:
            return None


class Owners(Resource):

    @property
    def owners(self):
        return load_from_yaml("owners.yaml", Owner).values()

    def get(self):
        schema = Owner.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.owners)
        return errors if errors else data

api.add_resource(Owners, '/owners/')
api.add_resource(Owner, '/owners/<int:object_id>')
