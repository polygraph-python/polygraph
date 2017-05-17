from polygraph.exceptions import PolygraphSchemaError
from polygraph.schema.introspection import TypeKind, type_definition
from polygraph.types.object_type import ObjectType
from polygraph.utils.strict_dict import StrictDict


def build_type_map(type_list):
    type_map = StrictDict()

    for type_ in type_list:
        typedef = type_definition(type_)
        kind = typedef.kind
        type_map[typedef.name] = type_
        if kind in (TypeKind.SCALAR, TypeKind.ENUM):
            continue
        elif kind in (TypeKind.LIST, TypeKind.NON_NULL):
            of_type = typedef.of_type
            subtype_map = build_type_map([of_type])
            type_map.update(subtype_map)

        elif kind == TypeKind.UNION:
            possible_types = typedef.possible_types
            subtype_map = build_type_map(possible_types)
            type_map.update(subtype_map)

        elif kind == TypeKind.OBJECT:
            field_types = []
            for field in (typedef.fields or []):
                field_types.append(field.return_type)
                field_types.extend(field.arg_types.values() if field.arg_types else [])
            subtype_map = build_type_map(field_types)
            type_map.update(subtype_map)

        elif kind == TypeKind.INPUT_OBJECT:
            # FIXME
            pass

        elif kind == TypeKind.INTERFACE:
            # FIXME
            pass

    return type_map


class Schema:
    def __init__(self, query: ObjectType, mutation=None, directives=None, additional_types=None):
        if not issubclass(query, ObjectType):
            raise PolygraphSchemaError("Query must be an ObjectType")
        self.query = query
        self.mutation = mutation
        self.directives = directives
        initial_types = additional_types or []
        initial_types.append(query)
        if mutation:
            initial_types.append(mutation)
        self.type_map = build_type_map(initial_types)
