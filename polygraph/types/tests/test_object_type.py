from collections import OrderedDict
from pprint import pformat
from unittest import TestCase

from graphql.type.scalars import GraphQLString

from polygraph.types.definitions import (
    PolygraphField,
    PolygraphNonNull,
    PolygraphObjectType,
)
from polygraph.types.decorators import field
from polygraph.types.scalar import String
from polygraph.types.object_type import ObjectType
from polygraph.types.basic_type import NonNull


class HelloWorldObject(ObjectType):
    """
    This is a test object
    """
    @field()
    def first(self) -> String:
        """First violin"""
        return "Stradivarius"

    @field()
    def second(self) -> NonNull(String):
        """Second fiddle"""
        pass

    @field(deprecation_reason="Third is dead")
    def third(self) -> NonNull(String):
        pass


# class ObjectTypeTest(TestCase):
#     def test_simple_object_type(self):
#         hello_world = HelloWorldObject()
#         expected = PolygraphObjectType(
#             name="HelloWorldObject",
#             description="This is a test object",
#             fields=OrderedDict({
#                 "first": PolygraphField(GraphQLString, None, None, None, "First violin"),
#                 "second": PolygraphField(
#                     PolygraphNonNull(GraphQLString), None, None, None, "Second fiddle"),
#                 "third": PolygraphField(
#                     PolygraphNonNull(GraphQLString), None, None, "Third is dead", None),
#             })
#         )
#         actual = hello_world.build_definition()
#         self.assertEqual(
#             expected, actual,
#             "\n\n{}\n\n!=\n\n{}".format(pformat(expected, indent=4), pformat(actual, indent=4))
#         )
