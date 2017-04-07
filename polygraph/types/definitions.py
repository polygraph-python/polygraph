from graphql.type.definition import GraphQLNonNull


class PolygraphNonNull(GraphQLNonNull):
    def __eq__(self, other):
        return isinstance(other, GraphQLNonNull) and self.of_type == other.of_type
