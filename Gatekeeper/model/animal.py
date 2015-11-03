from flask import request
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_restful import Resource

from Gatekeeper import app
from Gatekeeper import zmq
from Gatekeeper.model.image import Image
from Gatekeeper.model.image import Images
from Gatekeeper.model.namespaced_schema import NamespacedSchema
from Gatekeeper.model.owner import Owner
from Gatekeeper.model.owner import Owners
from Gatekeeper.model.util import fields_from_request
from Gatekeeper.model.util import load_from_yaml

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

sizes = ["small", "medium", "large"]
genders = ["female", "male"]
statuses = ["unavailable", "available", "foster", "adopted", "tbpd"]


class Animal(Resource):

    class ModelView(NamespacedSchema):
        name = ma.Str()
        ageRange = ma.Str(attribute='age_range')
        birthDate = ma.DateTime(attribute='birthdate')
        birthDateExact = ma.Bool(attribute='birthdate_exact')
        sizeRange = ma.Str(attribute='size_range')
        weight = ma.Float()
        gender = ma.Str()
        status = ma.Str()
        breed = ma.Str()
        group = ma.Str()
        color = ma.Str()
        trained = ma.Bool()
        goodWith = ma.Nested('Good_With', attribute='good_with')
        notes = ma.Str()
        primaryImages = ma.Hyperlinks({
            'xsmall': {'url': ma.AbsoluteURLFor('image', object_id='<image_primary>', size='xsmall'), 'method': 'GET'},
            'small': {'url': ma.AbsoluteURLFor('image', object_id='<image_primary>', size='small'), 'method': 'GET'},
            'medium': {'url': ma.AbsoluteURLFor('image', object_id='<image_primary>', size='medium'), 'method': 'GET'},
            'large': {'url': ma.AbsoluteURLFor('image', object_id='<image_primary>', size='large'), 'method': 'GET'}
        })
        metadata = ma.Nested('Metadata')

        class Good_With(ma.Schema):
            children = ma.Bool()
            dogs = ma.Bool()
            cats = ma.Bool()

        class Metadata(ma.Schema):
            created = ma.DateTime()
            updated = ma.DateTime()


    @classmethod
    def from_json(self, json_dict):
        schema = self.ModelView()
        data, error = schema.load(json_dict)
        return self(**data), error

    def __init__(self, name=None):
        self.object_id = None
        self.name = name
        self.birthdate = None
        self.birthdate_exact = False
        # self.tags = [] # new feature (v2)
        self.size_range = None  # constrained list
        self.weight = None  # free form
        self.gender = None  # constrained list
        self.status = None  # constrained list
        self.breed = None  # free form - populated from data dictionary
        self.group = None  # free form - populated from data dictionary
        self.color = None  # free form - populated from data dictionary
        self.good_with = {
            'children': False,  # bool
            'dogs': False,  # bool
            'cats': False  # bool
        }
        self.owners = []  # list of IDs (FK)
        self.images = []  # list of IDs (FK)
        self.image_primary = -1  # ID (FK)
        self.notes = None  # free form
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


@api.resource('/dogs/<int:object_id>')
class Dog(Animal):
    ages = ["puppy", "young", "adult", "senior"]

    class ModelView(Animal.ModelView):
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'DELETE'},
            'owners': {'url': ma.AbsoluteURLFor('dog_owners', object_id='<object_id>'), 'method': 'GET'},
            'images': {'url': ma.AbsoluteURLFor('dog_images', object_id='<object_id>'), 'method': 'GET'}
        })

        class Meta:
            name = 'dog'
            plural_name = 'dogs'

     
    def __init__(self, name=None):
        super().__init__(name)
        self.age_range = None  # constrained list
        self.trained = False  # bool

    @api.resource('/dogs/<int:object_id>/owners', endpoint='dog_owners')
    class Owners(Resource):
        pass

    @api.resource('/dogs/<int:object_id>/images', endpoint='dog_images')
    class Images(Resource):
        pass

    def load(self, dog_id):
        try:
            dogs = load_from_yaml("dogs.yaml", Dog)
            return dogs[dog_id]
        except IndexError:
            return None


@api.resource('/dogs')
class Dogs(Resource):

    @property
    def dogs(self):
        return load_from_yaml("dogs.yaml", Dog).values()

    def get(self):
        schema = Dog.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data

    def post(self):
        dog, errors = Dog.from_json(request.json)
        if errors:
            return errors

        dog.object_id = 0  # in a real app we'd have a new ID from the DB
        dog_json, errors = Dog.ModelView().dump(dog)

        zmq.publish("ANIMAL", "Created a dog named {0}".format(dog.name))
        return errors if errors else dog_json, 201

