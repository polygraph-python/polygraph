from graphql.type.definition import GraphQLObjectType


def graphql_objects_equal(object_A: GraphQLObjectType,
                          object_B: GraphQLObjectType):
    return (
        object_A.name == object_B.name and
        object_A.fields == object_B.fields and
        object_A.interfaces == object_B.interfaces and
        object_A.is_type_of == object_B.is_type_of and
        object_A.description == object_B.description
    )
