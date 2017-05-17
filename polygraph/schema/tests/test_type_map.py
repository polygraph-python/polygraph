from unittest import TestCase

from polygraph.schema.schema import Schema
from polygraph.types import (
    ID,
    Boolean,
    Float,
    Int,
    List,
    NonNull,
    ObjectType,
    String,
    Union,
    field,
)


class Person(ObjectType):
    @field
    def name(self) -> NonNull(String):
        pass

    @field
    def age(year: Int) -> String:
        pass


class Animal(ObjectType):
    @field
    def can_walk(self) -> Boolean:
        pass


class Query(ObjectType):
    @field
    def characters(self) -> List(Union(Animal, Person)):
        pass


class TypeMapTest(TestCase):
    def test_type_map_builder(self):
        schema = Schema(query=Query, additional_types=[ID])
        type_map = schema.type_map
        self.assertEqual(type_map["Animal"], Animal)
        self.assertEqual(type_map["Person"], Person)
        self.assertEqual(type_map["Animal|Person"], Union(Animal, Person))
        self.assertEqual(type_map["Boolean"], Boolean)
        self.assertEqual(type_map["ID"], ID)
        self.assertNotIn(Float, type_map.values())  # Float was not defined anywhere
