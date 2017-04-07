from collections import OrderedDict

from graphql.type.definition import GraphQLObjectType
from marshmallow import Schema, SchemaOpts

from polygraph.utils.trim_docstring import trim_docstring


class ObjectTypeOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.name = getattr(meta, 'name', None)
        self.description = getattr(meta, 'description', None)


class ObjectType(Schema):
    OPTIONS_CLASS = ObjectTypeOpts

    def __init__(self, only=(), exclude=(), prefix='', strict=None,
                 many=False, context=None, load_only=(), dump_only=(),
                 partial=False):
        super().__init__(only, exclude, prefix, strict,
                         many, context, load_only, dump_only, partial)
        self.name = self.opts.name or self.__class__.__name__
        self.description = self.opts.description or trim_docstring(self.__doc__)

    def build_definition(self):
        field_map = OrderedDict()
        for fieldname, field in self.fields.items():
            field_map[fieldname] = field.build_definition()
        return GraphQLObjectType(name=self.name,
                                 fields=field_map,
                                 description=self.description)
