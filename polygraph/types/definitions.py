from graphql.type.definition import GraphQLNonNull, GraphQLObjectType, GraphQLField


class SlotReprMixin:
    def __repr__(self):
        slot_values = ["{}={}".format(slot, getattr(self, slot)) for slot in self.__slots__]
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(slot_values)
        )


class PolygraphNonNull(GraphQLNonNull):
    def __eq__(self, other):
        return isinstance(other, GraphQLNonNull) and self.of_type == other.of_type


class PolygraphField(SlotReprMixin, GraphQLField):
    pass


class PolygraphObjectType(GraphQLObjectType):
    def __repr__(self):
        return "{}(name={}, fields={}, interfaces={}, is_type_of={}, description={})".format(
            self.__class__.__name__,
            repr(self.name),
            repr(self.fields),
            repr(self.interfaces),
            repr(self.is_type_of),
            repr(self.description),
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.name == other.name and
            self.fields == other.fields and
            self.interfaces == other.interfaces and
            self.is_type_of == other.is_type_of and
            self.description == other.description
        )
