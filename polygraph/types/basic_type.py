from polygraph.exceptions import PolygraphValueError


class PolygraphType:
    """Represents a Polygraph GraphQL type"""
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
