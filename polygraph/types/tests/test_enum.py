from unittest import TestCase

from polygraph.exceptions import PolygraphValueError
from polygraph.types.api import typedef
from polygraph.types.enum import EnumType


class Colours(EnumType):
    RED = "The colour of fury"
    GREEN = "The colour of envy"
    BLUE = "The colour of sloth"


class Shapes(EnumType):
    RECTANGLE = "A quadrangle"
    SQUARE = "Also a quadrangle"
    RHOMBUS = "Yet another quadrangle"


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
