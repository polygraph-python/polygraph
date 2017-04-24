from collections import OrderedDict
from functools import wraps
from inspect import signature

from typing import Tuple

from polygraph.types.api import get_type_class
from polygraph.exceptions import PolygraphSchemaError
from polygraph.types.basic_type import PolygraphInputType, PolygraphOutputType
from polygraph.utils.trim_docstring import trim_docstring


class Field:
    __slots__ = ["name", "return_type", "description", "arg_types", "deprecation_reason",
                 "is_deprecated", "resolver"]

    def __init__(self, name, return_type, description=None, arg_types=None,
                 deprecation_reason=None, resolver=None):
        self.name = name
        self.return_type = return_type
        self.description = description
        self.arg_types = arg_types
        self.deprecation_reason = deprecation_reason
        self.is_deprecated = bool(deprecation_reason)
        self.resolver = resolver

    def __get__(self, instance, owner_class):
        if instance is None:
            # Allows access to the Field object through the class definition
            # This does mean fields cannot be defined as classmethods though
            return self
        return self.resolver.__get__(instance, owner_class)


def validate_field_types(field: Field):
    not_input_type = [
        name for name, type_ in field.arg_types.items()
        if not issubclass(get_type_class(type_), PolygraphInputType)
    ]

    if not_input_type:
        raise PolygraphSchemaError(
            "{}: Fields {} must be subclasses of "
            "PolygraphInputType".format(field.name, not_input_type)
        )

    return_type = get_type_class(field.return_type)
    if not issubclass(return_type, PolygraphOutputType):
        raise PolygraphSchemaError("Field return type must be an instance of PolygraphOutputType")


def validate_method_annotations(method):
    """
    Checks that method has no non-annotated arguments, and that the annotated types
    are valid
    """
    method_name = method.__name__
    sig = signature(method)
    arguments = [p for p in sig.parameters.values() if p.name not in ("self", "cls")]

    non_annotated = [p for p in arguments if p.annotation == p.empty]
    if non_annotated:
        field_names = ", ".join(p.name for p in non_annotated)
        raise PolygraphSchemaError(
            "{}: Fields {} must be annotated".format(method_name, field_names)
        )


def _obtain_field_types(method) -> Tuple[dict, PolygraphOutputType]:
    """
    Returns a (arg_type_map, return_type) tuple, where arg_type_map is a
    map between arguments and their types; and return_type is the field type
    """
    validate_method_annotations(method)
    special_args = ["self", "cls"]
    sig = signature(method)
    parameters = [p for p in sig.parameters.values() if p.name not in special_args]
    arg_types = OrderedDict((p.name, p.annotation) for p in parameters)
    return_type = sig.return_annotation
    return arg_types, return_type


def field(name=None, deprecation_reason=None):
    def inner(method):
        arg_types, return_type = _obtain_field_types(method)

        @wraps(method)
        def wrapper(self, **kwargs):
            typed_args = {arg: arg_types[arg](val) for arg, val in kwargs.items()}
            return_val = method(self, **typed_args)
            return return_type(return_val)

        description = trim_docstring(method.__doc__)
        field_name = name or method.__name__
        field = Field(
            name=field_name,
            return_type=return_type,
            arg_types=arg_types,
            deprecation_reason=deprecation_reason,
            description=description,
            resolver=wrapper,
        )
        return field
    return inner
