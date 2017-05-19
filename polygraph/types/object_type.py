from polygraph.types.basic_type import PolygraphOutputType, PolygraphType
from polygraph.types.field import field


class ObjectType(PolygraphOutputType, PolygraphType):
    """
    GraphQL Objects represent a list of named fields, each of which yield
    a value of a specific type.
    """

    def __init__(self, root=None):
        self.root = root

    @staticmethod
    def field(func=None, *, name=None, deprecation_reason=None):
        return field(func, name, deprecation_reason)
