from polygraph.exceptions import PolygraphSchemaError
from polygraph.types.api import get_type_class
from polygraph.types.basic_type import PolygraphInputType, PolygraphType
from polygraph.types.definitions import TypeKind


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

    class Type:
        kind = TypeKind.INPUT_OBJECT


def validate_input_object_schema(input_object_class):
    attributes = (getattr(input_object_class, value) for value in dir(input_object_class))
    input_values = [attr for attr in attributes if isinstance(attr, InputValue)]

    if len(input_values) < 1:
        raise PolygraphSchemaError("Input objects require at least one InputValue attribute")

    names = [value.name for value in input_values]
    if len(set(names)) != len(input_values):
        raise PolygraphSchemaError("Input object values must be unique")

    return_types = [get_type_class(value.return_type) for value in input_values]
    if any(not issubclass(t, PolygraphInputType) for t in return_types):
        raise PolygraphSchemaError("Input object values must be subclasses of PolygraphInputType")
