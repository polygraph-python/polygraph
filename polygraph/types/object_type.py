import inspect
from collections import OrderedDict

from polygraph.types.basic_type import PolygraphOutputType, PolygraphType


class ObjectType(PolygraphOutputType, PolygraphType, dict):
    """
    GraphQL Objects represent a list of named fields, each of which yield
    a value of a specific type.
    """

    @classmethod
    def get_field_map(cls):
        field_map = OrderedDict()
        for _, method in inspect.getmembers(cls, predicate=inspect.ismethod):
            if hasattr(method, '__fieldname__') and hasattr(method, '__field__'):
                fieldname = method.__fieldname__
                field = method.__field__
                field_map[fieldname] = field
        return field_map
