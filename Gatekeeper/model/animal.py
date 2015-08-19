from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
from functools import lru_cache
from random import randint
import yaml

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

# For temporary YAML data only
# ==============================================================================
_DOGS= []

@lru_cache(maxsize=2)
def import_dogs_from_YAML():
    try:
        with open('data.yaml','r') as stream:
            for dog in yaml.safe_load_all(stream):
                _new_dog = Dog()

                for key, value in dog.items():
                    setattr(_new_dog, key, value)

                _new_dog.image_primary = randint(100, 1000)

                _DOGS.append(_new_dog)
    except OSError:
        print('Error: Cannot read from specified YAML file...')

# ==============================================================================

def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


class Animal(Resource):

    class ViewModel(ma.Schema):

        class Meta: ordered = True

        #id = ma.Int(attribute='object_id')

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

    def __init__(self):
        self.object_id = None

    def __repr__(self):
        _result = [("{key}='{value}'".format(key=key, value=self.__dict__[key])) for key in self.__dict__]
        return '<{0}({1})>'.format(self.__class__.__name__, ', '.join(_result))

    def get(self, object_id):
        instance = self.load(object_id)
        schema = self.ViewModel(only=fields_from_request(request))
        data, errors = schema.dump(instance)
        return errors if errors else data

    def load(self, object_id):
        pass


class Dog(Animal):

    from datetime import datetime

    _age_range = ['puppy','young','adult','senior']
    _gender = ['male','female']
    _size_range = ['small','medium','large']
    _status = ['unavailable', 'available', 'foster', 'adopted', 'tbpd']

    class ViewModel(Animal.ViewModel):

        class Good_With(ma.Schema):
            children = ma.Bool()
            dogs = ma.Bool()
            cats = ma.Bool()

        class Metadata(ma.Schema):
            created = ma.DateTime()
            updated = ma.DateTime()

        name = ma.Str()
        ageRange = ma.Str(attribute='age_range')
        birthdate = ma.DateTime()
        birthdate_exact = ma.Bool()
        sizeRange = ma.Str(attribute='size_range')
        weight = ma.Float()
        gender = ma.Str()
        status = ma.Str()
        breed = ma.Str()
        group = ma.Str()
        color = ma.Str()
        goodWith = ma.Nested('Good_With', attribute='good_with')
        trained = ma.Bool()
        notes = ma.Str()
        links = ma.Hyperlinks({
            'self': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'GET'},
            'update': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'PUT'},
            'delete': {'url': ma.AbsoluteURLFor('dog', object_id='<object_id>'), 'method': 'DELETE'},
            'owners': {'url': ma.AbsoluteURLFor('dog_owners', object_id='<object_id>'), 'method': 'GET'},
            'images': {'url': ma.AbsoluteURLFor('dog_images', object_id='<object_id>'), 'method': 'GET'}
        })
        primaryImages = ma.Hyperlinks({
            'xsmall': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='xsmall'), 'method': 'GET'},
            'small': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='small'), 'method': 'GET'},
            'medium':{'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='medium'), 'method': 'GET'},
            'large': {'url': ma.AbsoluteURLFor('images', object_id='<image_primary>', size='large'), 'method': 'GET'}
        })
        metadata = ma.Nested('Metadata')

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    class Owners(Resource):
        pass

    class Images(Resource):
        pass

    def __init__(self):

        _time = self.datetime.utcnow().replace(microsecond = 0)

        super(Dog, self).__init__()
        self.name = None
        #self.tags = [] # new feature (v2)
        self.age_range = None # constrained list
        self.birthdate = None # UTC DateTime
        self.birthdate_exact = False # bool
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
        self.image_primary = None # ID (FK)
        self.trained = False # bool
        self.notes = None # free form
        self.metadata = {
            'created': _time, # UTC DateTime (no microseconds)
            'updated': _time # UTC DateTime (no microseconds)
        }
        # self.links - ModelView
        #   self
        #   owners
        #   images
        #   images.primary

    def load(self, object_id):
        import_dogs_from_YAML() # For temporary YAML data only
        try:
            return [d for d in _DOGS if d.object_id == object_id][0]
        except IndexError:
            return None

class Dogs(Resource):

    def get(self):
        instance = self.load()
        schema = Dog.ViewModel(only=fields_from_request(request), many=True)
        data, errors = schema.dump(instance)
        return errors if errors else data

    def load(self):
        import_dogs_from_YAML() # For temporary YAML data only
        try:
            return _DOGS
        except:
            return None


class Owner(Resource):
    pass

class Owners(Resource):
    pass

class Image(Resource):
    pass

class Images(Resource):
    pass


api.add_resource(Dogs, '/dogs/')
api.add_resource(Dog, '/dogs/<int:object_id>')
api.add_resource(Dog.Owners, '/dogs/<int:object_id>/owners', endpoint='dog_owners')
api.add_resource(Dog.Images, '/dogs/<int:object_id>/images', endpoint='dog_images')
api.add_resource(Images, '/images/<int:object_id>/')
