from functools import wraps

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.basic_type import (
    PolygraphOutputType,
    PolygraphType,
    PolygraphTypeMeta,
)
from polygraph.types.definitions import TypeKind


type_builder_registry = {}


def type_builder_cache(method):
    @wraps(method)
    def wrapper(cls, *args):
        unique_args = frozenset(args)
        if (cls, unique_args) in type_builder_registry:
            return type_builder_registry[(cls, unique_args)]
        else:
            return_val = method(cls, *args)
            type_builder_registry[(cls, unique_args)] = return_val
            return return_val
    return wrapper


class TypeBuilderMeta(PolygraphTypeMeta):
    def __getitem__(self, value):
        try:
            return self.__new__(self, *value)
        except TypeError:
            return self.__new__(self, value)


class List(PolygraphOutputType, PolygraphType, metaclass=TypeBuilderMeta):
    """
    A GraphQL list is a special collection type which declares the
    type of each item in the List (referred to as the item type of
    the list).

    List values are serialized as ordered lists, where
    each item in the list is serialized as per the item type.
    """

    @type_builder_cache
    def __new__(cls, type_):
        type_name = typedef(type_).name

        def __new_from_value__(cls, value):
            if value is None:
                return None
            ret_val = [type_(v) for v in value]
            return list.__new__(cls, ret_val)

        class Type:
            name = "[{}]".format(type_name)
            description = "A list of {}".format(type_name)
            kind = TypeKind.LIST
            of_type = type_

        name = "List__" + type_name
        bases = (List, list)
        attrs = {"__new__": __new_from_value__, "Type": Type}
        return type(name, bases, attrs)


class NonNull(PolygraphType, metaclass=TypeBuilderMeta):
    """
    Represents a type for which null is not a valid result.
    """
    @type_builder_cache
    def __new__(cls, type_):
        type_name = typedef(type_).name

        if issubclass(type, NonNull):
            raise TypeError("NonNull cannot modify NonNull types")

        class Type:
            name = type_name + "!"
            description = "A non-nullable version of {}".format(type_name)
            kind = TypeKind.NON_NULL
            of_type = type_

        def __new_from_value__(cls, value):
            if value is None:
                raise PolygraphValueError("Non-nullable value cannot be None")
            return type_.__new__(cls, value)

        name = "NonNull__" + type_name
        bases = (NonNull, type_, )
        attrs = {"__new__": __new_from_value__, "Type": Type}
        return type(name, bases, attrs)
