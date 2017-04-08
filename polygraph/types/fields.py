from collections import OrderedDict

from graphql.type.scalars import GraphQLInt, GraphQLString
from marshmallow import fields

from polygraph.types.definitions import PolygraphField, PolygraphNonNull


class PolygraphFieldMixin:
    def __init__(self, type_, description=None, nullable=False, args=None,
                 deprecation_reason=None, **additional_args):
        super().__init__()
        self.type_ = type_
        self.description = description
        self.nullable = nullable
        self.args = args or OrderedDict()
        self.deprecation_reason = deprecation_reason

    def build_definition(self):
        if self.nullable:
            base_type = self.type_
        else:
            base_type = PolygraphNonNull(self.type_)
        return PolygraphField(
            type=base_type,
            args=self.args,
            deprecation_reason=self.deprecation_reason,
            description=self.description,
        )


class ScalarFieldMixin(PolygraphFieldMixin):
    base_type = None

    def __init__(self, description=None, nullable=False, args=None,
                 deprecation_reason=None, **additional_args):
        super().__init__(self.base_type, description, nullable,
                         args, deprecation_reason, **additional_args)


class String(ScalarFieldMixin, fields.String):
    base_type = GraphQLString


class Int(ScalarFieldMixin, fields.Int):
    base_type = GraphQLInt
