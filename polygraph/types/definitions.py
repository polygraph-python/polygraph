from enum import Enum
from collections import namedtuple


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


Field = namedtuple(
    "Field",
    [
        "name",
        "return_type",
        "description",
        "arg_types",
        "deprecation_reason",
        "is_deprecated",
    ]
)


TypeDefinition = namedtuple(
    "TypeDefinition",
    [
        "kind",
        "name",
        "description",
        "possible_types",
        "fields",
        "interfaces",
        "enum_values",
        "input_fields",
        "of_type",
    ]
)
