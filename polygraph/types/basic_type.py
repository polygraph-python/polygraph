from functools import wraps

from polygraph.exceptions import PolygraphSchemaError, PolygraphValueError
from polygraph.types.definitions import TypeDefinition, TypeKind
from polygraph.utils.trim_docstring import trim_docstring


def typedef(type_):
    return type_.__type


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


class PolygraphTypeMeta(type):
    def __new__(cls, name, bases, namespace):
        default_description = trim_docstring(namespace.get("__doc__", ""))
        if "Type" in namespace:
            meta = namespace["Type"]
        else:
            classes = [cls] + list(bases)
            classes = [b for b in bases if hasattr(b, "Type")]
            if classes:
                meta = classes[0].Type
            else:
                meta = None

        if meta:
            namespace["__type"] = TypeDefinition(
                kind=getattr(meta, "kind"),
                name=getattr(meta, "name", name) or name,
                description=getattr(meta, "description", default_description),
                fields=None,  # FIXME
                possible_types=getattr(meta, "possible_types", None),
                interfaces=None,  # FIXME
                enum_values=None,  # FIXME
                input_fields=None,  # FIXME
                of_type=getattr(meta, "of_type", None)
            )

        return super(PolygraphTypeMeta, cls).__new__(cls, name, bases, namespace)

    def __str__(self):
        return str(typedef(self).name)

    def __or__(self, other):
        """
        Allows creation of union types using `|`, e.g.

        > x = String | Int
        """
        return Union(self, other)


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
        try:
            typed_val = super(Scalar, cls).__new__(cls, value, *args, **kwargs)
        except ValueError as exc:
            raise PolygraphValueError(exc)
        return typed_val

    class Type:
        kind = TypeKind.SCALAR


class Interface(PolygraphOutputType, PolygraphType):
    """
    GraphQL Interfaces represent a list of named fields and their
    arguments. GraphQL objects can then implement an interface, which
    guarantees that they will contain the specified fields.
    """

    class Type:
        kind = TypeKind.INTERFACE


class Union(PolygraphOutputType, PolygraphType):
    """
    GraphQL Unions represent an object that could be one of a list of
    GraphQL Object types, but provides for no guaranteed fields between
    those types.
    """
    @type_builder_cache
    def __new__(cls, *types):
        types = set(types)
        assert len(types) >= 2, "Unions must consist of more than 1 type"
        bad_types = [t for t in types if not issubclass(t, PolygraphType)]
        if bad_types:
            message = "All types must be subclasses of PolygraphType. Invalid values: "\
                      "{}".format(", ".join(bad_types))
            raise PolygraphSchemaError(message)
        type_names = [typedef(t).name for t in types]

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
            kind = TypeKind.UNION

        name = "Union__" + "_".join(type_names)
        bases = (Union, )
        attrs = {"__new__": __new_from_value__}
        return type(name, bases, attrs)


class List(PolygraphType):
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


class NonNull(PolygraphType):
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


class InputObject(PolygraphInputType, PolygraphType):
    """
    An Input Object defines a set of input fields; the input fields
    are either scalars, enums, or other input objects. This allows
    arguments to accept arbitrarily complex structs.
    """

    class Type:
        kind = TypeKind.INPUT_OBJECT
