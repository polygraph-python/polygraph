from enum import Enum

from polygraph.types.basic_type import (
    PolygraphInputType,
    PolygraphOutputType,
    PolygraphType,
    PolygraphTypeMeta,
)
from polygraph.types.definitions import TypeKind


class EnumValue(PolygraphType):
    __slots__ = ["name", "description", "is_deprecated", "deprecation_reason"]

    def __init__(self, name, description=None, deprecation_reason=None):
        self.name = name
        self.description = description
        self.is_deprecated = bool(deprecation_reason)
        self.deprecation_reason = deprecation_reason

    def __repr__(self):
        return "EnumValue('{}')".format(self.name)

    class Type:
        name = "__EnumValue"


class EnumTypeMeta(PolygraphTypeMeta):
    def __new__(cls, name, bases, namespace):
        enum_values = {}
        for key, desc in namespace.items():
            if not key.startswith("_"):
                desc = namespace.get(key)
                enum_values[key] = EnumValue(name=key, description=desc)
        enum = Enum(name, enum_values)
        namespace.update(**enum.__members__)
        return super(EnumTypeMeta, cls).__new__(cls, name, bases, namespace)


class EnumType(PolygraphInputType, PolygraphOutputType, metaclass=EnumTypeMeta):
    """
    GraphQL Enums are a variant on the Scalar type, which represents one
    of a finite set of possible values.

    GraphQL Enums are not references for a numeric value, but are unique
    values in their own right. They serialize as a string: the name of
    the represented value.
    """

    class Type:
        kind = TypeKind.ENUM
