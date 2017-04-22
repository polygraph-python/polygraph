from unittest import TestCase

from polygraph.types.api import typedef
from polygraph.types.scalar import Float, Int, String
from polygraph.types.type_builder import List, NonNull
from polygraph.types.union import Union


class TestTypeDefinition(TestCase):

    def test_names_of_scalars(self):
        type_names = [
            (String, "String"),
            (Int, "Int"),
            (Float, "Float"),
        ]
        for type_, name in type_names:
            self.assertEqual(typedef(type_).name, name)

    def test_names_of_built_types(self):
        type_names = [
            (List(String), "[String]"),
            (Union(Int, String, List(String)), "Int|String|[String]"),
            (NonNull(Int), "Int!"),
            (NonNull(List(String)), "[String]!")
        ]
        for type_, name in type_names:
            self.assertEqual(typedef(type_).name, name)
