from unittest import TestCase

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.decorators import field
from polygraph.types.object_type import ObjectType
from polygraph.types.scalar import Int, String
from polygraph.types.type_builder import NonNull


class HelloWorldObject(ObjectType):
    """
    This is a test object
    """
    @field()
    def greet_world(self) -> String:
        """Generic message to the world"""
        return "Hello world!"

    @field()
    def greet_you(self, your_name: NonNull(String)) -> NonNull(String):
        """Greeting by name"""
        return "Hello, {}!".format(your_name)

    @field(deprecation_reason="Wrong return type")
    def bad_resolver(self) -> Int:
        return "three"


class SimpleObjectTypeTest(TestCase):
    def test_object_type_definition(self):
        type_info = typedef(HelloWorldObject)
        self.assertEqual(type_info.name, "HelloWorldObject")
        self.assertEqual(type_info.description, "This is a test object")
        self.assertEqual(
            set([f.name for f in type_info.fields]),
            set(["greet_world", "greet_you", "bad_resolver"]),
        )

    def test_bare_resolver(self):
        hello_world = HelloWorldObject()
        self.assertEqual(hello_world.greet_world(), String("Hello world!"))
        self.assertEqual(hello_world.greet_you(your_name="Bill"), String("Hello, Bill!"))

    def test_resolver_argument(self):
        hello_world = HelloWorldObject()
        with self.assertRaises(PolygraphValueError):
            hello_world.greet_you(your_name=None)

    def test_bad_resolver(self):
        hello_world = HelloWorldObject()
        with self.assertRaises(PolygraphValueError):
            hello_world.bad_resolver()
