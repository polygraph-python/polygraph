from collections import OrderedDict
from unittest import TestCase

from graphql.type.definition import GraphQLField, GraphQLObjectType
from graphql.type.scalars import GraphQLString

from polygraph.types.fields import String
from polygraph.types.object_type import ObjectType
from polygraph.types.tests.helpers import graphql_objects_equal


class HelloWorldObject(ObjectType):
    """
    This is a test object
    """
    test = String(description="Test string field", nullable=True)


class ObjectTypeTest(TestCase):
    def test_simple_object_type(self):
        hello_world = HelloWorldObject()
        expected = GraphQLObjectType(
            name="HelloWorldObject",
            description="This is a test object",
            fields=OrderedDict({
                "test": GraphQLField(
                    GraphQLString, None, None, None, "Test string field"),
            })
        )
        actual = hello_world.build_definition()
        self.assertTrue(graphql_objects_equal(expected, actual))
