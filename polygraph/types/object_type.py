from polygraph.types.basic_type import PolygraphOutputType, PolygraphType
from polygraph.types.definitions import TypeKind


class ObjectType(PolygraphOutputType, PolygraphType, dict):
    """
    GraphQL Objects represent a list of named fields, each of which yield
    a value of a specific type.
    """

    class Type:
        kind = TypeKind.OBJECT
