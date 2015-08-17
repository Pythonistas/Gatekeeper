from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
from datetime import datetime
import yaml


api = Api(app, prefix='/api/latest')
ma = Marshmallow(app)


def fields_from_request(request):
    fields = request.args.get('fields')
    return ma.split(',') if fields else None


class Animal(Resource):
    """description of Animal goes here"""

    _gender = ['Male','Female']

    class _Schema(ma.Schema):

        class Meta: ordered = True

        id = ma.Int(attribute='object_id')
        name = ma.Str()
        age = ma.Int()
        weight = ma.Int()
        gender = ma.Str()

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

    def __init__(self,
            object_id = None,
            name = '',
            age = 0,
            weight = 0,
            gender = ''
        ):
        self.object_id = object_id
        self.name = name
        self.age = age
        self.weight = weight
        self.gender = gender

    def get(self, object_id):
        instance = self.__class__(object_id)
        schema = self._Schema(only=fields_from_request(request))
        data, errors = schema.dump(instance)
        return errors if errors else data

    def load(self, object_id):
        pass


class Dog(Animal):
    """description of Dog goes here"""

    from datetime import datetime

    _age_range = ['Puppy','Young','Adult','Senior']
    _group = ['Hearding','Hound','Non-Sporting','Sporting','Terrier','Toy','Working','FoundationStockService','Miscellaneous']
    _size_range = ['Small','Medium','Large']
    _status = ['Unavailable', 'Available', 'Foster', 'Adopted', 'TBPD']

    class _Schema_Good_With(ma.Schema):
        children = ma.Bool()
        dogs = ma.Bool()
        cats = ma.Bool()

    class _Schema_Metadata(ma.Schema):
        created = ma.DateTime()
        updated = ma.DateTime()

    class _Schema_Links(ma.Schema):

        class Meta: ordered = True

        href = ma.AbsoluteURLFor('dog', object_id='<object_id>')
        rel = ma.Str()
        method = ma.Str()

    class _Schema(Animal._Schema):
        ageRange = ma.Str(attribute='age_range')
        sizeRange = ma.Str(attribute='size_range')
        status = ma.Str()
        breed = ma.Str()
        group = ma.Str()
        color = ma.Str()
        goodWith = ma.Nested('_Schema_Good_With', attribute='good_with')
        trained = ma.Bool()
        notes = ma.Str()
        links = ma.Nested('_Schema_Links')
        metadata = ma.Nested('_Schema_Metadata')

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    def __init__(self,
            object_id = None,
            name = '',
            age = 0,
            weight = 0,
            gender = '',
            age_range = '', #_age_range[0]
            size_range = '', #_size_range[0]
            status = '',
            breed = '',
            group = '', #_group[0]
            color = '',
            good_with = {'children': False, 'dogs': False, 'cats': False},
            trained = False,
            notes = '',
        ):

        _time = self.datetime.utcnow().replace(microsecond = 0)

        super(Dog, self).__init__(object_id, name, age, weight, gender)
        self.age_range = age_range
        self.size_range = size_range
        self.status = status
        self.breed = breed
        self.group = group
        self.color = color
        self.good_with = good_with
        self.trained = trained
        self.notes = notes
        self.links = {'object_id': object_id, 'rel': 'self', 'method': 'GET'}
        self.metadata = {'created': _time, 'updated': _time}

    def __repr__(self):
        _result = [("{key}='{value}'".format(key=key, value=self.__dict__[key])) for key in self.__dict__]
        return '<{0}({1})>'.format(self.__class__.__name__, ', '.join(_result))

    def load(self, object_id):
        pass

class Dogs(Resource):
    """description of Dogs goes here"""

    @property
    def dogs(self):
        return [Dog(i) for i in range(5)]

    def get(self):
        schema = Dog._Schema(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data

    def load(self):
        pass


api.add_resource(Dog, '/dogs/<int:object_id>')
api.add_resource(Dogs, '/dogs/')
