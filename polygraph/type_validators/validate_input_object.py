from polygraph.exceptions import PolygraphTypeError
from polygraph.types import InputValue
from polygraph.types.api import get_type_class
from polygraph.types.basic_type import PolygraphInputType


def validate_input_object(input_object_class):
    attributes = (getattr(input_object_class, value) for value in dir(input_object_class))
    input_values = [attr for attr in attributes if isinstance(attr, InputValue)]

    if len(input_values) < 1:
        raise PolygraphTypeError("Input objects require at least one InputValue attribute")

    names = [value.name for value in input_values]
    if len(set(names)) != len(input_values):
        raise PolygraphTypeError("Input object values must be unique")

    return_types = [get_type_class(value.return_type) for value in input_values]
    if any(not issubclass(t, PolygraphInputType) for t in return_types):
        raise PolygraphTypeError("Input object values must be subclasses of PolygraphInputType")
