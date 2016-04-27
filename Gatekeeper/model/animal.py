from flask import request
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_restful import Resource

from Gatekeeper import app
from Gatekeeper.model.image import Image
from Gatekeeper.model.image import Images
from Gatekeeper.model.namespaced_schema import NamespacedSchema
from Gatekeeper.model.owner import Owner
from Gatekeeper.model.owner import Owners
from Gatekeeper.model.util import fields_from_request

## MONGO DB
from pymongo import MongoClient
from bson.objectid import ObjectId as BSON_ObjectId


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

    def __init__(self):
        self.name = None
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

    def internal_get(self, object_id):
        instance = self.load(object_id)
        if instance:
            schema = self.ModelView(only=fields_from_request(request))
            data, errors = schema.dump(instance)
            return errors if errors else data
        # TODO: return error object if nothing could be loaded

    def load(self, object_id):
        pass

    @classmethod
    def new_from_dict(cls, dict):
        this = cls()

        for key, value in dict.items():
            setattr(this, key, value)

        return this
        # TODO: return error if contains unrecognized attributes
        # TODO: return error if missing required attributes

@api.resource('/dogs/<string:object_id>')
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

    def __init__(self):
        super().__init__()
        self.age_range = None  # constrained list
        self.trained = False  # bool

    @api.resource('/dogs/<string:object_id>/owners', endpoint='dog_owners')
    class Owners(Resource):
        pass

    @api.resource('/dogs/<string:object_id>/images', endpoint='dog_images')
    class Images(Resource):
        pass

    def get(self, object_id):
        return self.internal_get(object_id)

    def load(self, object_id):

        ## MONGO DB
        dogs_collection = app.config['GATEKEEPERDB'].Dogs
        document = dogs_collection.find_one({ '_id': BSON_ObjectId(object_id) })
        dog = Dog.new_from_dict(document)

        return dog

    def put(self, object_id):

        ## MONGO DB
        dogs_collection = app.config['GATEKEEPERDB'].Dogs
        dog = dogs_collection.update({ '_id': BSON_ObjectId(object_id)}, { '$set': request.json }, multi = False)

        return dog


@api.resource('/dogs/')
class Dogs(Resource):

    @property
    def dogs(self):

        ## MONGO DB
        dogs_collection = app.config['GATEKEEPERDB'].Dogs
        cursor = dogs_collection.find()
        dogs = [Dog.new_from_dict(document) for document in cursor]

        return dogs

    def get(self):
        schema = Dog.ModelView(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data

    def post(self):

        ## MONGO DB
        dogs_collection = app.config['GATEKEEPERDB'].Dogs
        # TODO: Create dog instance before attempting to create new record
        dog_id = dogs_collection.insert(request.json)

        return {'url': api.url_for(Dog, object_id = dog_id, _external = True)}
