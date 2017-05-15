from unittest import TestCase

from polygraph.exceptions import PolygraphTypeError
from polygraph.type_validators import validate_input_object
from polygraph.types.input_object import InputObject, InputValue
from polygraph.types.lazy_type import LazyType
from polygraph.types.scalar import String
from polygraph.types.tests.helper import Person


class SampleInput(InputObject):
    name = InputValue(String, name="name")
    age = InputValue(LazyType("Int", module_name="polygraph.types.scalar"), name="age")


class NoInput(InputObject):
    pass


class DuplicateInputName(InputObject):
    name = InputValue(String, name="name")
    second_name = InputValue(String, name="name")


class NonInputType(InputObject):
    person = InputValue(Person)


class InputObjectTest(TestCase):
    def test_validate_good_schema(self):
        self.assertIsNone(validate_input_object(SampleInput))

    def test_validate_bad_schema(self):
        for bad_input_object in [NoInput, DuplicateInputName, NonInputType]:
            with self.subTest(input_object=bad_input_object):
                with self.assertRaises(PolygraphTypeError):
                    validate_input_object(bad_input_object)
