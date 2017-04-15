from enum import Enum
from typing import List


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


class Field:
    def __init__(self, name, return_type, description=None,
                 arg_types=None, deprecation_reason=None):
        self.name = name
        self.return_type = return_type
        self.description = description
        self.arg_types = arg_types
        self.deprecation_reason = deprecation_reason
        self.is_deprecated = bool(deprecation_reason)


class TypeDefinition:
    def __init__(self, kind: TypeKind, name: str, fields: List[Field]=None,
                 interfaces=None, enum_values=None, input_fields=None, of_type=None):
        self.kind = kind
        self.name = name
        self.fields = fields
        self.interfaces = interfaces
        self.enum_values = enum_values
        self.input_fields = input_fields
        self.of_type = of_type
