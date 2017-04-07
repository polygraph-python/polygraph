from collections import OrderedDict

from graphql.type.definition import GraphQLField, GraphQLNonNull
from graphql.type.scalars import GraphQLString
from marshmallow import fields


class String(fields.String):
    def __init__(self, description, nullable=False, args=None,
                 deprecation_reason=None, **additional_args):
        super().__init__()
        self.description = description
        self.nullable = nullable
        self.args = args or OrderedDict()
        self.deprecation_reason = deprecation_reason

    def build_definition(self):
        if self.nullable:
            base_type = GraphQLString
        else:
            base_type = GraphQLNonNull(GraphQLString)
        return GraphQLField(
            type=base_type,
            args=self.args,
            deprecation_reason=self.deprecation_reason,
            description=self.description,
        )
