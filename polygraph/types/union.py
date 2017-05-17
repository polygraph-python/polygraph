from functools import wraps

from polygraph.exceptions import PolygraphSchemaError, PolygraphValueError
from polygraph.types.basic_type import PolygraphOutputType, PolygraphType
from polygraph.types.type_builder import TypeBuilderMeta, type_builder_cache
from polygraph.utils.deduplicate import deduplicate


def flatten(iterable):
    for arg in iterable:
        if issubclass(arg, Union):
            yield from flatten(arg.__type.possible_types)
        else:
            yield arg


def deduplicate_union_args(method):
    @wraps(method)
    def wrapper(cls, *types):
        types = list(deduplicate(flatten(types)))
        return method(cls, *types)
    return wrapper


class Union(PolygraphOutputType, PolygraphType, metaclass=TypeBuilderMeta):
    """
    GraphQL Unions represent an object that could be one of a list of
    GraphQL Object types, but provides for no guaranteed fields between
    those types.
    """

    @deduplicate_union_args
    @type_builder_cache
    def __new__(cls, *types):
        assert len(types) >= 2, "Unions must consist of more than 1 type"
        bad_types = [t for t in types if not issubclass(t, PolygraphType)]
        if bad_types:
            message = "All types must be subclasses of PolygraphType. Invalid values: "\
                      "{}".format(", ".join(bad_types))
            raise PolygraphSchemaError(message)
        type_names = [t.__name__ for t in types]

        def __new_from_value__(cls, value):
            if not any(isinstance(value, t) for t in types):
                valid_types = ", ".join(type_names)
                message = "{} is an invalid value type. "\
                          "Valid types: {}".format(type(value), valid_types)
                raise PolygraphValueError(message)
            return value

        class Type:
            name = "|".join(type_names)
            description = "One of {}".format(", ".join(type_names))
            possible_types = types

        name = "Union__" + "_".join(type_names)
        bases = (Union, )
        attrs = {"__new__": __new_from_value__, "Type": Type}
        return type(name, bases, attrs)
