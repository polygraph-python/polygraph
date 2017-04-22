from types import SimpleNamespace
from unittest import TestCase

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.decorators import field
from polygraph.types.nonnull import NonNull
from polygraph.types.object_type import ObjectType
from polygraph.types.scalar import Int, String


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


class ObjectResolver(ObjectType):
    @field()
    def name(self) -> NonNull(String):
        return self.full_name()

    @field()
    def age_in_2017(self) -> NonNull(Int):
        return 2017 - self.root.birthyear

    @field()
    def always_none(self) -> String:
        return self.root.address

    @field()
    def greeting(self) -> HelloWorldObject:
        return HelloWorldObject()

    def full_name(self):
        return self.root.first_name + " " + self.root.last_name


class ObjectResolverTest(TestCase):
    def setUp(self):
        obj = SimpleNamespace(
            first_name="John",
            last_name="Smith",
            birthyear=2000,
            address=None,
        )
        self.object_type = ObjectResolver(obj)

    def test_method_is_not_automatically_field(self):
        type_info = typedef(self.object_type)
        fields = set([f.name for f in type_info.fields])
        self.assertEqual(
            fields,
            set(["name", "age_in_2017", "always_none", "greeting"]),
        )
        self.assertNotIn("full_name", fields)

    def test_simple_resolver(self):
        self.assertEqual(self.object_type.name(), "John Smith")
        self.assertEqual(self.object_type.age_in_2017(), 17)
        self.assertEqual(self.object_type.always_none(), None)

    def test_resolve_to_object(self):
        greeting = self.object_type.greeting()
        self.assertEqual(greeting.greet_world(), "Hello world!")
