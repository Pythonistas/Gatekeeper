from Gatekeeper import app
from marshmallow import SchemaOpts, post_dump, pre_load
from flask_marshmallow import Marshmallow

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

    @pre_load(raw=True)
    def unwrap_envelope(self, data, many):
        key = self.opts.plural_name if many else self.opts.name
        return data[key]

    @post_dump(raw=True)
    def wrap_with_envelope(self, data, many):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}