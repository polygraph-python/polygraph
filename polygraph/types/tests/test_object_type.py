from collections import OrderedDict
from pprint import pformat
from unittest import TestCase

from graphql.type.scalars import GraphQLString

from polygraph.types.definitions import (
    PolygraphField,
    PolygraphNonNull,
    PolygraphObjectType,
)
from polygraph.types.fields import Int, String
from polygraph.types.object_type import ObjectType


class ObjectTypeTest(TestCase):
    maxDiff = None

    def test_simple_object_type(self):
        class HelloWorldObject(ObjectType):
            """
            This is a test object
            """
            first = String(description="First violin", nullable=True)
            second = String(description="Second fiddle", nullable=False)
            third = String(deprecation_reason="Third is dead")

        hello_world = HelloWorldObject()
        expected = PolygraphObjectType(
            name="HelloWorldObject",
            description="This is a test object",
            fields=OrderedDict({
                "first": PolygraphField(GraphQLString, None, None, None, "First violin"),
                "second": PolygraphField(
                    PolygraphNonNull(GraphQLString), None, None, None, "Second fiddle"),
                "third": PolygraphField(
                    PolygraphNonNull(GraphQLString), None, None, "Third is dead", None),
            })
        )
        actual = hello_world.build_definition()
        self.assertEqual(
            expected, actual,
            "\n\n{}\n\n!=\n\n{}".format(pformat(expected, indent=4), pformat(actual, indent=4))
        )
        # self.assertTrue(graphql_objects_equal(expected, actual))

    def test_object_type_meta(self):
        class MetaObject(ObjectType):
            """
            This docstring is _not_ the description
            """
            count = Int()

            class Meta:
                name = "Meta"
                description = "Actual meta description is here"

        meta = MetaObject()
        self.assertEqual(meta.description, "Actual meta description is here")
        self.assertEqual(meta.name, "Meta")
