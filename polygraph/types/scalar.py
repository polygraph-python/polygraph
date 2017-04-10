from polygraph.types.basic_type import Scalar


class Int(Scalar, int):
    """
    Represents a signed 32‐bit numeric non‐fractional value.
    """

    @classmethod
    def parse_literal(cls, ast):
        return int(ast)

    @classmethod
    def render_value(cls, value):
        return int(value)


class String(Scalar, str):
    """
    The String scalar type represents textual data, represented as
    UTF‐8 character sequences.
    """

    @classmethod
    def parse_literal(cls, ast):
        return str(ast)

    @classmethod
    def render_value(cls, value):
        return str(value)


class Float(Scalar, float):
    """
    The Float scalar type represents signed double‐precision fractional
    values as specified by IEEE 754.
    """

    @classmethod
    def parse_literal(cls, ast):
        return float(ast)

    @classmethod
    def render_value(cls, value):
        return float(value)


class Boolean(Scalar, object):
    """
    The Boolean scalar type represents true or false.
    """

    def __init__(self, value):
        self.value = bool(value)

    def __bool__(self):
        return self.value

    @classmethod
    def parse_literal(cls, ast):
        return bool(ast)

    @classmethod
    def render_value(cls, value):
        return bool(value)


class ID(Scalar, str):
    """
    The ID type represents a unique ID of a GraphQL resource
    """

    @classmethod
    def parse_literal(cls, ast):
        return str(ast)

    @classmethod
    def render_value(cls, value):
        return str(value)
