from unittest import TestCase

from polygraph.exceptions import PolygraphSchemaError
from polygraph.types.field import (
    field,
    validate_field_types,
    validate_method_annotations,
)
from polygraph.types.lazy_type import LazyType
from polygraph.types.object_type import ObjectType
from polygraph.types.scalar import Int, String
from polygraph.types.tests.helper import Person


lazy_string = LazyType("String", "polygraph.types.scalar")
lazy_animal = LazyType("Animal", "polygraph.types.tests.helper")


class FieldTest(TestCase):

    def test_validate_field_types(self):

        class Test(ObjectType):
            @field()
            def valid_field(self, arg1: Int) -> String:
                pass

            @field()
            def also_valid_field(self, arg1: lazy_string) -> lazy_animal:
                pass

            @field()
            def bad_argument_type(self, arg1: Person) -> String:  # ObjectType is not valid input
                pass

            @field()
            def bad_lazy_argument_type(self, arg1: lazy_animal) -> String:
                pass

            @field()
            def bad_return_type(self, arg1: String) -> str:
                pass

        self.assertIsNone(validate_field_types(Test.valid_field))
        self.assertIsNone(validate_field_types(Test.also_valid_field))

        with self.assertRaises(PolygraphSchemaError):
            validate_field_types(Test.bad_argument_type)

        with self.assertRaises(PolygraphSchemaError):
            validate_field_types(Test.bad_lazy_argument_type)

        with self.assertRaises(PolygraphSchemaError):
            validate_field_types(Test.bad_return_type)

    def test_validate_method_annotations(self):
        def unannotated_argument(self, arg1) -> String:
            pass

        def unannotated_return_type(self, arg1: String, arg2: Int):
            pass

        def fully_annotated_method(self, arg1: String, arg2: Int) -> lazy_animal:
            pass

        with self.assertRaises(PolygraphSchemaError):
            validate_method_annotations(unannotated_argument)

        with self.assertRaises(PolygraphSchemaError):
            validate_method_annotations(unannotated_return_type)

        self.assertIsNone(validate_method_annotations(fully_annotated_method))
