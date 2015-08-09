from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from flask import request
from datetime import datetime


api = Api(app, prefix='/api/v1')


class Animal(Resource):

    class _Schema(Schema):
        name = fields.Str()
        birth_date = fields.Date()

    def get(self):
        fields = request.args.get('fields')
        fields_list = fields.split(',') if fields else None
        schema = self._Schema(only=fields_list)
        data, errors = schema.dump(self)
        return errors if errors else data


class Dog(Animal):

    class _Schema(Animal._Schema):
        breed = fields.Str()

    def __init__(self):
        self.name = 'fred'
        self.breed = 'bison'
        self.birth_date = datetime.now()

api.add_resource(Dog, '/dog/')
