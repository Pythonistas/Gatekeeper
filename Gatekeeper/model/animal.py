from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
from datetime import datetime

from Gatekeeper.model.util import fields_from_request, load_from_yaml
from Gatekeeper.model.image import Image, Images
from Gatekeeper.model.owner import Owner, Owners

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

ages = ["puppy", "young", "adult", "senior"]
sizes = ["small", "medium", "large"]
genders = ["female", "male"]
statuses = ["unavailable", "available", "foster", "adopted", "tbpd"]

class Animal(Resource):

    class ModelView(ma.Schema):
        name = ma.Str()
        birthDate = ma.DateTime(attribute='birthdate')
        birthDateExact = ma.Bool(attribute='birthdate_exact')
        ageRange = ma.Str(attribute='age_range')
        sizeRange = ma.Str(attribute='size_range')
        weight = ma.Float()
        gender = ma.Str()
        status = ma.Str()
        breed = ma.Str()
        group = ma.Str()
        color = ma.Str()
        goodWith = ma.Nested('Good_With', attribute='good_with')
        notes = ma.Str()
        primaryImages = ma.Hyperlinks({
            'xsmall': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='xsmall'), 'method': 'GET'},
            'small': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='small'), 'method': 'GET'},
            'medium':{'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='medium'), 'method': 'GET'},
            'large': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='large'), 'method': 'GET'}
        })
        metadata = ma.Nested('Metadata')

        class Good_With(ma.Schema):
            children = ma.Bool()
            dogs = ma.Bool()
            cats = ma.Bool()

        class Metadata(ma.Schema):
            created = ma.DateTime()
            updated = ma.DateTime()

        # TODO use NamespacedSchema technique instead
        # see http://marshmallow.readthedocs.org/en/latest/extending.html#example-enveloping-revisited
        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

    def __init__(self):
        self.object_id = None
        self.name = None
        self.birthdate = None
        self.birthdate_exact = False
        #self.tags = [] # new feature (v2)
        self.age_range = None # constrained list
        self.size_range = None # constrained list
        self.weight = None # free form
        self.gender = None # constrained list
        self.status = None # constrained list
        self.breed = None # free form - populated from data dictionary
        self.group = None # free form - populated from data dictionary
        self.color = None # free form - populated from data dictionary
        self.good_with = {
            'children': False, # bool
            'dogs': False, # bool
            'cats': False # bool
        } 
        self.owners = [] # list of IDs (FK)
        self.images = [] # list of IDs (FK)
        self.image_primary = -1 # ID (FK)
        self.notes = None # free form
        self.metadata = {
            'created': None,
            'updated': None,
        }

    def get(self, object_id):
        instance = self.load(object_id)
        if instance:
            schema = self.ModelView(only=fields_from_request(request))
            data, errors = schema.dump(instance)
            return errors if errors else data
        # TODO: return error object if nothing could be loaded

    def load(self, object_id):
        pass


class Dog(Animal):

    class ModelView(Animal.ModelView):
        trained = ma.Bool()
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'DELETE'},
            'owners': {'url': ma.AbsoluteURLFor('dog_owners', object_id='<object_id>'), 'method': 'GET'},
            'images': {'url': ma.AbsoluteURLFor('dog_images', object_id='<object_id>'), 'method': 'GET'}
        })

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    def __init__(self):
        super().__init__()
        self.trained = False # bool

    class Owners(Resource):
        pass

    class Images(Resource):
        pass

    def load(self, dog_id):
        try:
            dogs = load_from_yaml("dogs.yaml", Dog)
            return dogs[dog_id]
        except IndexError:
            return None

class Dogs(Resource):

    @property
    def dogs(self):
        return load_from_yaml("dogs.yaml", Dog).values()

    def get(self):
        schema = Dog.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data


api.add_resource(Dogs, '/dogs/')
api.add_resource(Dog, '/dogs/<int:object_id>')
api.add_resource(Dog.Owners, '/dogs/<int:object_id>/owners', endpoint='dog_owners')
api.add_resource(Dog.Images, '/dogs/<int:object_id>/images', endpoint='dog_images')
