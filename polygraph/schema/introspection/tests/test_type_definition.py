from unittest import TestCase

from polygraph.schema.introspection import type_definition
from polygraph.schema.introspection.models import TypeKind
from polygraph.types import (
    ID,
    Float,
    InputObject,
    InputValue,
    Int,
    List,
    NonNull,
    ObjectType,
    String,
    Union,
    field,
)


class MockObject(ObjectType):
    @field()
    def field_one(self, value: String) -> Int:
        return 1


class OtherObject(ObjectType):
    @field()
    def field_two(self, value: String) -> List[Int]:
        return [1, 2, 3]

    class Type:
        name = "Test"


class MockInputObject(InputObject):
    input_one = InputValue(String)


class TestTypeDefinition(TestCase):

    def test_type_kind(self):
        type_kinds = [
            (String, TypeKind.SCALAR),
            (Int, TypeKind.SCALAR),
            (ID, TypeKind.SCALAR),
            (MockObject, TypeKind.OBJECT),
            (OtherObject, TypeKind.OBJECT),
            (Union[MockObject, OtherObject], TypeKind.UNION),
            (List(NonNull(String)), TypeKind.LIST),
            (List(String), TypeKind.LIST),
            (NonNull(List(String)), TypeKind.NON_NULL),
            (NonNull(String), TypeKind.NON_NULL),
            (MockInputObject, TypeKind.INPUT_OBJECT),
        ]
        for type_, kind in type_kinds:
            self.assertEqual(type_definition(type_).kind, kind)

    def test_names_of_scalars(self):
        type_names = [
            (String, "String"),
            (Int, "Int"),
            (Float, "Float"),
        ]
        for type_, name in type_names:
            self.assertEqual(type_definition(type_).name, name)
