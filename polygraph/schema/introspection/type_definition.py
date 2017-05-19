from types import SimpleNamespace

from polygraph.types import (
    EnumType,
    EnumValue,
    Field,
    InputObject,
    InputValue,
    Interface,
    List,
    NonNull,
    ObjectType,
    Scalar,
    Union,
)
from polygraph.utils.trim_docstring import trim_docstring

from .models import TypeDefinition, TypeKind


def _kind(type_):
    if issubclass(type_, NonNull):
        return TypeKind.NON_NULL
    elif issubclass(type_, Scalar):
        return TypeKind.SCALAR
    elif issubclass(type_, EnumType):
        return TypeKind.ENUM
    elif issubclass(type_, Union):
        return TypeKind.UNION
    elif issubclass(type_, ObjectType):
        return TypeKind.OBJECT
    elif issubclass(type_, InputObject):
        return TypeKind.INPUT_OBJECT
    elif issubclass(type_, List):
        return TypeKind.LIST
    elif issubclass(type_, Interface):
        return TypeKind.INTERFACE


def _meta(type_):
    return getattr(type_, "Type", SimpleNamespace())


def _name(type_):
    name = getattr(_meta(type_), "name", type_.__name__)
    return name


def _description(type_):
    default_description = trim_docstring(type_.__doc__)
    description = getattr(_meta(type_), "description", default_description)
    return description


def _fields(type_):
    return [value for value in type_.__dict__.values() if isinstance(value, Field)] or None


def _possible_types(type_):
    return getattr(_meta(type_), "possible_types", None)


def _interfaces(type_):
    return getattr(_meta(type_), "interfaces", None)


def _enum_values(type_):
    return [value for value in type_.__dict__.values() if isinstance(value, EnumValue)] or None


def _input_fields(type_):
    return [value for value in type_.__dict__.values() if isinstance(value, InputValue)] or None


def _of_type(type_):
    return getattr(_meta(type_), "of_type", None)


def type_definition(type_) -> TypeDefinition:
    return TypeDefinition(
        kind=_kind(type_),
        name=_name(type_),
        description=_description(type_),
        fields=_fields(type_),
        possible_types=_possible_types(type_),
        interfaces=_interfaces(type_),
        enum_values=_enum_values(type_),
        input_fields=_input_fields(type_),
        of_type=_of_type(type_),
    )
