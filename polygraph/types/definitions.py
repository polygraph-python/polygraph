from graphql.type.definition import (
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
)

from polygraph.utils.attr_repr_mixin import AttrReprMixin


class PolygraphNonNull(GraphQLNonNull):
    def __eq__(self, other):
        return isinstance(other, GraphQLNonNull) and self.of_type == other.of_type


class PolygraphField(AttrReprMixin, GraphQLField):
    pass


class PolygraphObjectType(AttrReprMixin, GraphQLObjectType):
    def __repr_attributes__(self):
        return ["name", "fields", "interfaces", "is_type_of", "description"]

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.name == other.name and
            self.fields == other.fields and
            self.interfaces == other.interfaces and
            self.is_type_of == other.is_type_of and
            self.description == other.description
        )
