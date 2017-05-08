from unittest import TestCase

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.enum import EnumType, EnumValue


class Colours(EnumType):
    RED = EnumValue("The colour of fury")
    GREEN = EnumValue("The colour of envy")
    BLUE = EnumValue("The colour of sloth")


class Shapes(EnumType):
    RECTANGLE = EnumValue("A quadrangle")
    SQUARE = EnumValue("Also a quadrangle")
    RHOMBUS = EnumValue("Yet another quadrangle")


class EnumTest(TestCase):

    def test_simple_enum(self):
        red = Colours.RED
        self.assertEqual(red.name, "RED")
        self.assertEqual(red.description, "The colour of fury")

        green = Colours.GREEN
        self.assertEqual(green.name, "GREEN")
        self.assertEqual(green.description, "The colour of envy")

        blue = Colours.BLUE
        self.assertEqual(blue.name, "BLUE")
        self.assertEqual(blue.description, "The colour of sloth")

    def test_enum_value(self):
        self.assertEqual(Colours(Colours.RED), Colours.RED)
        with self.assertRaises(PolygraphValueError):
            Colours("RED")

    def test_enum_values_dont_mix(self):
        with self.assertRaises(PolygraphValueError):
            Colours(Shapes.RECTANGLE)

        with self.assertRaises(PolygraphValueError):
            Shapes(Colours.BLUE)

    def test_enum_type(self):
        colour_type = typedef(Colours)
        self.assertEqual(len(colour_type.enum_values), 3)

    def test_enum_value_name(self):
        class NamedValue(EnumType):
            ORIGINAL = EnumValue("Name is ORIGINAL")
            REPLACED = EnumValue("Name is NOT_REPLACED", name="NOT_REPLACED")

        self.assertEqual(NamedValue.ORIGINAL.name, "ORIGINAL")
        self.assertEqual(NamedValue.REPLACED.name, "NOT_REPLACED")
