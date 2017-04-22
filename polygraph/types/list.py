from polygraph.types.api import typedef
from polygraph.types.basic_type import PolygraphOutputType, PolygraphType
from polygraph.types.definitions import TypeKind
from polygraph.types.type_builder import TypeBuilderMeta, type_builder_cache


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
