from polygraph.types.basic_type import PolygraphOutputType, PolygraphType


class ObjectType(PolygraphOutputType, PolygraphType, dict):
    """
    GraphQL Objects represent a list of named fields, each of which yield
    a value of a specific type.
    """

    def __init__(self, root=None):
        self.root = root
