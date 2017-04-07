from collections import OrderedDict
from unittest import TestCase

from graphql.type.definition import GraphQLField, GraphQLObjectType
from graphql.type.scalars import GraphQLString

from polygraph.types.definitions import PolygraphNonNull
from polygraph.types.fields import String
from polygraph.types.object_type import ObjectType
from polygraph.types.tests.helpers import graphql_objects_equal


class HelloWorldObject(ObjectType):
    """
    This is a test object
    """
    first = String(description="First violin", nullable=True)
    second = String(description="Second fiddle", nullable=False)
    third = String(deprecation_reason="Third is dead")


class ObjectTypeTest(TestCase):
    def test_simple_object_type(self):
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
