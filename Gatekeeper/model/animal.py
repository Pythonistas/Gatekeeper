from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import Schema, fields, post_dump
from flask import request
from datetime import datetime

api = Api(app, prefix='/api/v1')


def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


class Animal(Resource):

    class _Schema(Schema):
        name = fields.Str()
        birth_date = fields.Date()

        @post_dump(raw=True)
        def wrap_with_envelope(self, data, many):
            key = self.get_envelope_key(many)
            return {key: data}

    def get(self, object_id):
        self.object_id = object_id

        schema = self._Schema(only=fields_from_request(request))
        data, errors = schema.dump(self)
        return errors if errors else data


class Dog(Animal):

    class _Schema(Animal._Schema):
        breed = fields.Str()
        url = fields.Str()

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    def __init__(self, object_id=None):
        self.object_id = object_id
        self.name = 'fred'
        self.breed = 'bison'
        self.birth_date = datetime.now()

    @property
    def url(self):
        return request.url


class Dogs(Resource):

    @property
    def dogs(self):
        return [Dog(i) for i in range(5)]

    def get(self):
        schema = Dog._Schema(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data


api.add_resource(Dog, '/dogs/<int:object_id>')
api.add_resource(Dogs, '/dogs/')
