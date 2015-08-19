from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
from datetime import datetime
import yaml

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)

ages    = ["puppy", "young", "adult", "senior"]
sizes   = ["small", "medium", "large"]
genders = ["female", "male"]
statuses= ["unavailable", "available", "foster", "adopted", "tbpd"]

def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


class Animal(Resource):

    class _Schema(ma.Schema):
        name = ma.Str()
        birth_date = ma.DateTime()

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

    def __init__(self):
        self.object_id = None
        self.name = None

    def get(self, object_id):
        instance = self.load(object_id)
        if instance:
            schema = self._Schema(only=fields_from_request(request))
            data, errors = schema.dump(instance)
            return errors if errors else data
        # TODO: return error object if nothing could be loaded

    def load(self, object_id):
        pass


class Dog(Animal):

    class _Schema(Animal._Schema):
        breed = ma.Str()
        links = ma.Hyperlinks({
            'self': ma.AbsoluteURLFor('dog', object_id='<object_id>')
        })

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    def __init__(self):
        super(Dog, self).__init__()
        self.breed = None
        self.birth_date = datetime.now()
        self.status = None
        self.color = None
        self.ageRange = None
        self.age = None
        self.weightRange = None
        self.weight = None
        self.gender = None
        self.goodWith = {}
        self.trained = False
        self.notes = None
        self.owners = None
        self.primaryImage = {}
        self.metadata = {}

    def load(self, dog_id):
        try:
            dogs = Dogs.load_from_yaml()
            return dogs[dog_id]
        except IndexError:
            return None

class Dogs(Resource):

    @staticmethod
    def load_from_yaml():
        dogs = []
        dog_id = 0
        try:
            with open("dogs.yaml", 'r') as stream:
                for data in yaml.safe_load(stream):
                    cur_dog = Dog()
                    cur_dog.object_id = dog_id
                    cur_dog.name = data['name']
                    cur_dog.status = data['status']
                    cur_dog.breed = data['breed']
                    cur_dog.color = data['color']
                    cur_dog.ageRange = data['ageRange']
                    cur_dog.age = data['age']
                    cur_dog.weightRange = data['weightRange']
                    cur_dog.weight = data['weight']
                    cur_dog.gender = data['gender']
                    cur_dog.trained = data['trained']
                    dogs.append(cur_dog)
                    dog_id += 1
        except OSError:
            print("File not found")
            return None
        return dogs

    @property
    def dogs(self):
        return Dogs.load_from_yaml()

    def get(self):
        schema = Dog._Schema(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data


api.add_resource(Dog, '/dogs/<int:object_id>')
api.add_resource(Dogs, '/dogs/')
