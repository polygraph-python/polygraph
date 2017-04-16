from collections import OrderedDict
from functools import wraps
from inspect import signature

from typing import Tuple

from polygraph.exceptions import PolygraphSchemaError
from polygraph.types.basic_type import PolygraphInputType, PolygraphOutputType
from polygraph.types.definitions import Field
from polygraph.utils.trim_docstring import trim_docstring


def _obtain_field_types(func) -> Tuple[dict, PolygraphOutputType]:
    """
    Returns a (arg_type_map, return_type) tuple, where arg_type_map is a
    map between arguments and their types; and return_type is the field type
    """
    special_args = ["self", "cls"]
    func_name = func.__name__
    sig = signature(func)
    return_type = sig.return_annotation
    parameters = [p for p in sig.parameters.values() if p.name not in special_args]
    non_annotated = [p for p in parameters if p.annotation == p.empty]
    if non_annotated:
        field_names = ", ".join(p.name for p in non_annotated)
        raise PolygraphSchemaError(
            "{}: Fields {} must be annotated".format(func_name, field_names)
        )

    not_subclassed = [p for p in parameters if not issubclass(p.annotation, PolygraphInputType)]
    if not_subclassed:
        field_names = ", ".join(p.name for p in not_subclassed)
        raise PolygraphSchemaError(
            "{}: Fields {} must be subclasses of PolygraphInputType".format(func_name, field_names)
        )
    if not issubclass(return_type, PolygraphOutputType):
        raise PolygraphSchemaError("Field return type must be an instance of PolygraphOutputType")
    arg_types = OrderedDict((p.name, p.annotation) for p in parameters)
    return arg_types, return_type


def field(rename_to=None, deprecation_reason=None):
    def inner(method):
        arg_types, return_type = _obtain_field_types(method)

        @wraps(method)
        def wrapper(self, **kwargs):
            typed_args = {arg: arg_types[arg](val) for arg, val in kwargs.items()}
            return_val = method(self, **typed_args)
            return return_type(return_val)

        description = trim_docstring(method.__doc__)
        name = rename_to or method.__name__
        wrapper.__field__ = Field(
            name=name,
            return_type=return_type,
            arg_types=arg_types,
            deprecation_reason=deprecation_reason,
            description=description,
            is_deprecated=bool(deprecation_reason),
        )
        return wrapper
    return inner
