from unittest import TestCase, skip

from polygraph.exceptions import PolygraphValueError
from polygraph.types.basic_type import NonNull
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
