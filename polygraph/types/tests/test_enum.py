from polygraph.types.enum import EnumType
from unittest import TestCase


class Colours(EnumType):
    RED = "The colour of fury"
    GREEN = "The colour of envy"
    BLUE = "The colour of sloth"


class EnumTest(TestCase):

    def test_simple_enum(self):
        red = Colours.RED.value
        self.assertEqual(red.name, "RED")
        self.assertEqual(red.description, "The colour of fury")

        green = Colours.GREEN.value
        self.assertEqual(green.name, "GREEN")
        self.assertEqual(green.description, "The colour of envy")

        blue = Colours.BLUE.value
        self.assertEqual(blue.name, "BLUE")
        self.assertEqual(blue.description, "The colour of sloth")

