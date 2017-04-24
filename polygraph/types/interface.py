from polygraph.types.basic_type import PolygraphOutputType, PolygraphType
from polygraph.types.definitions import Field
from polygraph.exceptions import PolygraphSchemaError


class Interface(PolygraphOutputType, PolygraphType):
    pass


def validate_interface_schema(interface_class):
    attributes = (
        getattr(interface_class, attr).__field__
        for attr in dir(interface_class)
        if hasattr(getattr(interface_class, attr), "__field__")
    )
    fields = [attr for attr in attributes if isinstance(attr, Field)]

    if len(fields) < 1:
        raise PolygraphSchemaError("Interfaces require at least one field")

    names = [field.name for field in fields]
    if len(set(names)) != len(names):
        raise PolygraphSchemaError("Interface field names should all be unique")

    if any(name.startswith("__") for name in names):
        raise PolygraphSchemaError("Interface field names cannot start with '__'")


