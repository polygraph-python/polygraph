from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.definitions import TypeDefinition, TypeKind
from polygraph.utils.trim_docstring import trim_docstring


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
        from polygraph.types.type_builder import Union
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


class InputObject(PolygraphInputType, PolygraphType):
    """
    An Input Object defines a set of input fields; the input fields
    are either scalars, enums, or other input objects. This allows
    arguments to accept arbitrarily complex structs.
    """

    class Type:
        kind = TypeKind.INPUT_OBJECT
