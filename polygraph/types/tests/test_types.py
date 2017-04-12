from unittest import TestCase, skip

from polygraph.exceptions import PolygraphValueError
from polygraph.types.basic_type import List, NonNull
from polygraph.types.scalar import Boolean, Int, String
from polygraph.utils.trim_docstring import trim_docstring


class TypeMetaTest(TestCase):
    def test_scalar_meta(self):
        self.assertEqual(Int._type.name, "Int")
        self.assertEqual(Int._type.description, trim_docstring(Int.__doc__))
        self.assertEqual(String._type.name, "String")
        self.assertEqual(String._type.description, trim_docstring(String.__doc__))
        self.assertEqual(Boolean._type.name, "Boolean")
        self.assertEqual(Boolean._type.description, trim_docstring(Boolean.__doc__))

    def test_type_string(self):
        self.assertEqual(str(Int), "Int")
        self.assertEqual(str(String), "String")
        self.assertEqual(str(Boolean), "Boolean")

    @skip("Not implemented yet")
    def test_type_subclass_doesnt_use_docstring_for_description(self):
        class FancyString(String):
            """Not the description"""
            pass

        self.assertEqual(FancyString._type.name, "String")
        self.assertNotEqual(FancyString._type.description, "Not the description")


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
