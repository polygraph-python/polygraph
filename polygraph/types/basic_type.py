import types

from polygraph.exceptions import PolygraphValueError
from polygraph.utils.trim_docstring import trim_docstring


class PolygraphTypeMeta(type):
    def __new__(cls, name, bases, namespace):
        default_description = trim_docstring(namespace.get("__doc__", ""))
        meta = namespace.pop("Type", types.SimpleNamespace())
        meta.description = getattr(meta, "description", default_description)
        meta.name = getattr(meta, "name", name) or name

        namespace["_type"] = meta

        return super(PolygraphTypeMeta, cls).__new__(cls, name, bases, namespace)

    def __str__(self):
        return str(self._type.name)


class PolygraphType(metaclass=PolygraphTypeMeta):
    pass


class PolygraphInputType:
    @classmethod
    def parse_literal(classmethod, ast):
        raise NotImplemented("Defined in subclasses")


class PolygraphOutputType:
    @classmethod
    def render_value(cls, value):
        raise NotImplemented("Defined in subclasses")


class Scalar(PolygraphInputType, PolygraphOutputType, PolygraphType):
    """A scalar represents a primitive value in GraphQL"""
    def __new__(cls, value, *args, **kwargs):
        if value is None:
            return None
        return super(Scalar, cls).__new__(cls, value, *args, **kwargs)


class Interface(PolygraphOutputType, PolygraphType):
    """
    GraphQL Interfaces represent a list of named fields and their
    arguments. GraphQL objects can then implement an interface, which
    guarantees that they will contain the specified fields.
    """


class Union(PolygraphOutputType, PolygraphType):
    """
    GraphQL Unions represent an object that could be one of a list of
    GraphQL Object types, but provides for no guaranteed fields between
    those types.
    """


class Listable(PolygraphType, list):
    def __new__(cls, value):
        if value is None:
            return None
        ret_val = [cls.of_type(v) for v in value]
        return super(Listable, cls).__new__(cls, ret_val)


class List(PolygraphType):
    """
    A GraphQL list is a special collection type which declares the
    type of each item in the List (referred to as the item type of
    the list).

    List values are serialized as ordered lists, where
    each item in the list is serialized as per the item type.
    """

    def __new__(cls, type_):
        type_name = type_._type.name

        class Type:
            name = "[{}]".format(type_name)
            description = "A list of {}".format(type_name)

        name = "List__" + type_name
        bases = (Listable, )
        attrs = {"Type": Type, "of_type": type_}
        return type(name, bases, attrs)


class NonNullable:
    def __new__(cls, value):
        if value is None:
            raise PolygraphValueError("Non-nullable value cannot be None")
        return super().__new__(cls, value)


class NonNull(PolygraphType):
    """
    Represents a type for which null is not a valid result.
    """
    def __new__(cls, type_):
        type_name = type_._type.name

        if issubclass(type, NonNullable):
            raise TypeError("NonNull cannot modify NonNull types")

        class Type:
            name = type_name + "!"
            description = "A non-nullable version of {}".format(type_name)

        name = "NonNull__" + type_name
        bases = (NonNullable, type_, )
        attrs = {"Type": Type}
        return type(name, bases, attrs)


class InputObject(PolygraphInputType, PolygraphType):
    """
    An Input Object defines a set of input fields; the input fields
    are either scalars, enums, or other input objects. This allows
    arguments to accept arbitrarily complex structs.
    """
