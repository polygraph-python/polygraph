from polygraph.types.basic_type import PolygraphInputType, PolygraphType


class InputValue:
    __slots__ = ["name", "return_type", "description", "default_value"]

    def __init__(self, return_type, name=None, description=None, default_value=None):
        self.name = name
        self.return_type = return_type
        self.description = description
        self.default_value = default_value


class InputObject(PolygraphInputType, PolygraphType):
    """
    An Input Object defines a set of input fields; the input fields
    are either scalars, enums, or other input objects. This allows
    arguments to accept arbitrarily complex structs.
    """
    pass
