from enum import Enum

from attr import attrib, attrs
from typing import Iterable


class TypeKind(Enum):
    SCALAR = "Represents scalar types such as Int, String, and Boolean. Scalars cannot have fields."
    OBJECT = "Object types represent concrete instantiations of sets of fields. "
    UNION = "Unions are an abstract type where no common fields are declared."
    INTERFACE = "Interfaces are an abstract type where there are common fields declared."
    ENUM = "Enums are special scalars that can only have a defined set of values."
    INPUT_OBJECT = "Input objects are composite types used as inputs into queries defined as a "\
                   "list of named input values."
    LIST = "Lists represent sequences of values in GraphQL."
    NON_NULL = "A Non‐null type is a type modifier: it wraps another type instance in the "\
               "ofType field. Non‐null types do not allow null as a response, and indicate "\
               "required inputs for arguments and input object fields."


@attrs(frozen=True)
class PolygraphType:
    kind = attrib()
    name = attrib(default=None)
    description = attrib(default=None)
    fields = attrib(default=tuple(), convert=tuple)
    interfaces = attrib(default=tuple(), convert=tuple)
    possible_types = attrib(default=tuple(), convert=tuple)
    enum_values = attrib(default=tuple(), convert=tuple)
    input_fields = attrib(default=tuple(), convert=tuple)
    of_type = attrib(default=None)

    def __call__(self, value):
        # TODO: Do validation of value here
        return PolygraphValue(type_=self, value=value)


@attrs(frozen=True)
class PolygraphInputValue:
    name = attrib()
    input_type = attrib()
    description = attrib(default=None)
    default_value = attrib(default=None)


@attrs(frozen=True)
class PolygraphField:
    name = attrib()
    return_type = attrib()
    description = attrib(default=None)
    args = attrib(default=tuple(), convert=tuple)
    is_deprecated = attrib(default=False)
    deprecation_reason = attrib(default=None)
    resolver = attrib(default=None)


@attrs(frozen=True)
class DeferredType:
    name = attrib()


@attrs(frozen=True)
class PolygraphValue:
    """Represents a typed value"""
    type_ = attrib()  # type: PolygraphType
    value = attrib()  # type: Object


def field(name, return_type, description=None, args=None, deprecation_reason=None, resolver=None):
    args = args or []
    return PolygraphField(
        name=name,
        description=description,
        args=args,
        return_type=return_type,
        deprecation_reason=deprecation_reason,
        is_deprecated=bool(deprecation_reason),
        resolver=resolver,
    )


def object_type(name, description=None, fields: Iterable[PolygraphField]=None, interfaces=None) \
        -> PolygraphType:
    fields = fields or []
    interfaces = interfaces or []
    return PolygraphType(
        kind=TypeKind.OBJECT,
        name=name,
        description=description,
        fields=fields,
        interfaces=interfaces,
    )


def scalar(name, description=None) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.SCALAR,
        name=name,
        description=description,
    )


def union(name, possible_types, description=None) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.UNION,
        name=name,
        description=description,
        possible_types=possible_types,
    )


def interface(name, description, fields) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.INTERFACE,
        name=name,
        description=description,
        fields=fields,
    )


def enum_type(name, description, enum_values) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.ENUM,
        name=name,
        description=description,
        enum_values=[e for e in enum_values],
    )


def input_object(name, description, input_fields) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.INPUT_OBJECT,
        name=name,
        description=description,
        input_fields=[f for f in input_fields],
    )


def list_type(of_type) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.LIST,
        of_type=of_type,
    )


def non_null(of_type) -> PolygraphType:
    return PolygraphType(
        kind=TypeKind.NON_NULL,
        of_type=of_type,
    )


Int = scalar(name="Int", description="Represents a signed 32‐bit numeric non‐fractional value.")
String = scalar(name="String", description="The String scalar type represents textual data, "
                                           "represented as UTF‐8 character sequences.")
Float = scalar(name="Float", description="The Float scalar type represents signed double‐precision "
                                         "fractional values as specified by IEEE 754.")
Boolean = scalar(name="Boolean", description="The Boolean scalar type represents true or false.")
