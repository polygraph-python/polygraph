from unittest import TestCase, skip

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.scalar import Boolean, Int, String
from polygraph.types.type_builder import List, NonNull
from polygraph.utils.trim_docstring import trim_docstring


class TypeMetaTest(TestCase):
    def test_scalar_meta(self):
        self.assertEqual(typedef(Int).name, "Int")
        self.assertEqual(typedef(Int).description, trim_docstring(Int.__doc__))
        self.assertEqual(typedef(String).name, "String")
        self.assertEqual(typedef(String).description, trim_docstring(String.__doc__))
        self.assertEqual(typedef(Boolean).name, "Boolean")
        self.assertEqual(typedef(Boolean).description, trim_docstring(Boolean.__doc__))

    def test_type_string(self):
        self.assertEqual(str(Int), "Int")
        self.assertEqual(str(String), "String")
        self.assertEqual(str(Boolean), "Boolean")

    @skip("Not implemented yet")
    def test_type_subclass_doesnt_use_docstring_for_description(self):
        class FancyString(String):
            """Not the description"""
            pass

        self.assertEqual(FancyString.__type.name, "String")
        self.assertNotEqual(FancyString.__type.description, "Not the description")


class NonNullTest(TestCase):
    def test_string(self):
        self.assertEqual(str(NonNull(String)), "String!")
        self.assertEqual(str(NonNull(Int)), "Int!")

    def test_nonnull_accepts_values(self):
        NonNullString = NonNull(String)
        self.assertEqual(NonNullString("test"), "test")

    def test_nonnull_doesnt_accept_none(self):
        NonNullString = NonNull(String)
        with self.assertRaises(PolygraphValueError):
            NonNullString(None)

    def test_cannot_have_nonnull_of_nonnull(self):
        NonNullString = NonNull(String)
        with self.assertRaises(TypeError):
            NonNull(NonNullString)

    def test_square_bracket_notation(self):
        self.assertEqual(NonNull(String), NonNull[String])


class ListTest(TestCase):

    def test_scalar_list(self):
        int_list = List(Int)
        self.assertEqual(str(int_list), "[Int]")
        self.assertEqual(int_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(int_list(None), None)
        with self.assertRaises(ValueError):
            int_list(["a", "b", "c"])

    def test_list_of_nonnulls(self):
        string_list = List(NonNull(String))
        self.assertEqual(str(string_list), "[String!]")
        self.assertEqual(string_list(["a", "b", "c"]), ["a", "b", "c"])
        with self.assertRaises(PolygraphValueError):
            string_list(["a", "b", "c", None])

    def test_square_bracket_notation(self):
        self.assertEqual(List(Int), List[Int])

