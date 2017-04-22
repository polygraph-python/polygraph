from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.basic_type import PolygraphType
from polygraph.types.definitions import TypeKind
from polygraph.types.type_builder import TypeBuilderMeta, type_builder_cache


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
