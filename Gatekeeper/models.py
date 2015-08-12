from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import Schema, fields, post_dump
from flask import request


api = Api(app, prefix='/api/latest')


class Animal(Resource):
    """description of Animal goes here"""

    _sex = ['Male','Female']


    class _Schema(Schema):
        
        class Meta: ordered = True

        id = fields.Int()
        name = fields.Str()
        age = fields.Int()
        weight = fields.Int()
        sex = fields.Str()


    def __init__(self):
        self.id = 0
        self.name = ''
        self.age = 0
        self.weight = 0
        self.sex = '' #_sex[0]


    def get(self):
        fields = request.args.get('fields')
        fields_list = fields.split(',') if fields else None
        schema = self._Schema(only=fields_list)
        data, errors = schema.dump(self)
        return errors if errors else data

    #def __repr__(self):
    #    _result = [("{key}='{value}'".format(key=key, value=self.__dict__[key])) for key in self.__dict__]
    #    return '<{0}({1})>'.format(self.__class__.__name__, ', '.join(_result))

    #def to_json_dict(self, *fields):
    #    """
    #    Returns a dictionary of properties, limited to those specified in fields, 
    #    or all public fields if fields is not specified.
    #    """

    #    if fields:
    #        return {self.__class__.__name__.lower(): {str(field): getattr(self, field) for field in fields}}
    #    else:
    #        return {self.__class__.__name__.lower(): self.__dict__}
            
class Dog(Animal):
    """description of Dog goes here"""

    from datetime import datetime

    _age_range = ['Puppy','Young','Adult','Senior']
    _group = ['Hearding','Hound','Non-Sporting','Sporting','Terrier','Toy','Working','FoundationStockService','Miscellaneous']
    _size_range = ['Small','Medium','Large']
    _status = ['Unavailable', 'Available', 'Foster', 'Adopted', 'TBPD']


    class _Schema_Good_With(Schema):
                        
        class Meta: ordered = True

        children = fields.Bool()
        dogs = fields.Bool()
        cats = fields.Bool()


    class _Schema_Links(Schema):
                        
        class Meta: ordered = True

        href = fields.Url('dog')
        rel = fields.Str()
        method = fields.Str()


    class _Schema_Metadata(Schema):
                        
        class Meta: ordered = True

        created = fields.DateTime()
        updated = fields.DateTime()


    class _Schema(Animal._Schema):

        age_range = fields.Str()
        size_range = fields.Str()
        status = fields.Str()
        breed = fields.Str()
        group = fields.Str()
        color = fields.Str()
        good_with = fields.Nested('_Schema_Good_With')
        trained = fields.Bool()
        notes = fields.Str()
        links = fields.Nested('_Schema_Links', many=True)
        metadata = fields.Nested('_Schema_Metadata')

        # Add an envelope to responses
        @post_dump(raw=True)
        def wrap(self, data, many):
            key = 'dogs' if many else 'dog'
            return { key: data }

    def __init__(self):

        _time = self.datetime.utcnow().replace(microsecond = 0)

        super().__init__()
        self.age_range = '' #_age_range[0]
        self.size_range = '' #_size_range[0]
        self.status = ''
        self.breed = ''
        self.group = '' #_group[0]
        self.color = ''
        self.good_with = {'children': False, 'dogs': False, 'cats': False}
        self.trained = False
        self.notes = ''
        self.links = [{'href': None, 'rel': 'self', 'method': 'GET'}, {'href': None, 'rel': 'edit', 'method': 'PUT'}, {'href': None, 'rel': 'delete', 'method': 'DELETE'}]
        self.metadata = {'created': _time, 'updated': _time}


api.add_resource(Dog, '/dogs/<id>', endpoint='dog')
api.add_resource(Dog, '/dogs/', endpoint='dogs')
