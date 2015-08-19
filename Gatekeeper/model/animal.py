from Gatekeeper import app
from flask_restful import Resource, Api
from marshmallow import post_dump
from flask_marshmallow import Marshmallow
from flask import request
from datetime import datetime

api = Api(app, prefix='/api/v1')
ma = Marshmallow(app)


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

    def __init__(self, object_id):
        self.object_id = object_id
        pass

    def get(self, object_id):
        instance = self.__class__(object_id)
        schema = self._Schema(only=fields_from_request(request))
        data, errors = schema.dump(instance)
        return errors if errors else data


class Dog(Animal):

    class _Schema(Animal._Schema):
        breed = ma.Str()
        links = ma.Hyperlinks({
            'self': ma.AbsoluteURLFor('dog', object_id='<object_id>')
        })

        @staticmethod
        def get_envelope_key(many):
            return 'dogs' if many else 'dog'

    def __init__(self, object_id):
        super(Dog, self).__init__(object_id)
        self.name = None
        self.breed = None
        self.birth_date = datetime.now()


class Dogs(Resource):

    @property
    def dogs(self):
        return [Dog(i) for i in range(5)]

    def get(self):
        schema = Dog._Schema(only=fields_from_request(request), many=True)
        data, errors = schema.dump(self.dogs)
        return errors if errors else data


api.add_resource(
    Dog, '/dogs/<int:object_id>', resource_class_args={'object_id': None})
api.add_resource(Dogs, '/dogs/')
