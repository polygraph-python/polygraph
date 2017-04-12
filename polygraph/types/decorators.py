from functools import wraps

from polygraph.types.basic_type import PolygraphOutputType
from polygraph.types.definitions import PolygraphField
from polygraph.utils.trim_docstring import trim_docstring


def field(rename_to=None, deprecation_reason=None):
    def inner(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            return method(self, *args, **kwargs)
        description = trim_docstring(method.__doc__)
        name = rename_to or method.__name__
        type_ = method.__annotations__.get("return")
        assert issubclass(type_, PolygraphOutputType)
        wrapper.__fieldname__ = name
        wrapper.__field__ = PolygraphField(
            type=type_,
            args=None,
            resolver=None,
            deprecation_reason=deprecation_reason,
            description=description,
        )
        return wrapper
    return inner
