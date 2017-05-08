from polygraph.exceptions import PolygraphValueError
from polygraph.types.basic_type import (
    PolygraphInputType,
    PolygraphOutputType,
    PolygraphTypeMeta,
)
from polygraph.types.definitions import EnumValue, TypeKind


class EnumTypeMeta(PolygraphTypeMeta):
    def __new__(cls, name, bases, namespace):
        for key, value in namespace.items():
            if type(value) == EnumValue:
                value.name = value.name or key
                value.parent = name
        return super().__new__(cls, name, bases, namespace)


class EnumType(PolygraphInputType, PolygraphOutputType, metaclass=EnumTypeMeta):
    """
    GraphQL Enums are a variant on the Scalar type, which represents one
    of a finite set of possible values.

    GraphQL Enums are not references for a numeric value, but are unique
    values in their own right. They serialize as a string: the name of
    the represented value.
    """

    def __new__(cls, value):
        if getattr(value, "parent", None) != cls.__name__:
            raise PolygraphValueError(
                "Only values belonging to {} are acceptable".format(cls.__name__)
            )
        return value

    class Type:
        kind = TypeKind.ENUM
