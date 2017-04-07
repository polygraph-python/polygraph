from collections import OrderedDict
from unittest import TestCase

from graphql.type.definition import GraphQLField, GraphQLObjectType
from graphql.type.scalars import GraphQLString

from polygraph.types.definitions import PolygraphNonNull
from polygraph.types.fields import String, Int
from polygraph.types.object_type import ObjectType
from polygraph.types.tests.helpers import graphql_objects_equal


class ObjectTypeTest(TestCase):
    def test_simple_object_type(self):
        class HelloWorldObject(ObjectType):
            """
            This is a test object
            """
            first = String(description="First violin", nullable=True)
            second = String(description="Second fiddle", nullable=False)
            third = String(deprecation_reason="Third is dead")

        hello_world = HelloWorldObject()
        expected = GraphQLObjectType(
            name="HelloWorldObject",
            description="This is a test object",
            fields=OrderedDict({
                "first": GraphQLField(GraphQLString, None, None, None, "First violin"),
                "second": GraphQLField(
                    PolygraphNonNull(GraphQLString), None, None, None, "Second fiddle"),
                "third": GraphQLField(
                    PolygraphNonNull(GraphQLString), None, None, "Third is dead", None),
            })
        )
        actual = hello_world.build_definition()
        self.assertTrue(graphql_objects_equal(expected, actual))

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
