from unittest import TestCase

from polygraph.exceptions import PolygraphSchemaError
from polygraph.types.field import field
from polygraph.types.interface import Interface, validate_interface_schema
from polygraph.types.scalar import String


class InterfaceValidationTest(TestCase):
    def test_valid_interface(self):

        class Humanoid(Interface):
            @field
            def name(self) -> String:
                pass  # pragma: no cover

        self.assertIsNone(validate_interface_schema(Humanoid))

    def test_interface_with_no_fields(self):

        class NoField(Interface):
            pass

        with self.assertRaises(PolygraphSchemaError):
            validate_interface_schema(NoField)

    def test_interface_with_duplicate_field_name(self):

        class Duplicate(Interface):
            @field
            def name(self) -> String:
                pass  # pragma: no cover

            @field(name="name")
            def other_name(self) -> String:
                pass  # pragma: no cover

        with self.assertRaises(PolygraphSchemaError):
            validate_interface_schema(Duplicate)

    def test_interface_with_invalid_field_name(self):

        class DunderscoredField(Interface):
            @field
            def __name(self) -> String:
                pass  # pragma: no cover

        with self.assertRaises(PolygraphSchemaError):
            validate_interface_schema(DunderscoredField)
