from flask_marshmallow import Marshmallow
from marshmallow import SchemaOpts
from marshmallow import post_dump
from marshmallow import pre_load

from Gatekeeper import app

ma = Marshmallow(app)


class NamespaceOpts(SchemaOpts):

    """Same as the default class Meta options, but adds "name" and
    "plural_name" options for enveloping.
    """

    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.name = getattr(meta, 'name', None)
        self.plural_name = getattr(meta, 'plural_name', self.name)


class NamespacedSchema(ma.Schema):
    OPTIONS_CLASS = NamespaceOpts

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        key = self.opts.plural_name if many else self.opts.name
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}
