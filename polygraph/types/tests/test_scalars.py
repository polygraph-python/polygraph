from unittest import TestCase

from polygraph.types.basic_type import typedef
from polygraph.types.scalar import ID, Boolean, Float, Int, String


class IntTest(TestCase):
    def test_class_types(self):
        x = Int(245)
        self.assertIsInstance(x, int)
        self.assertIsInstance(x, Int)
        self.assertEqual(Int(245) + 55, 300)

        y = Int("506")
        self.assertIsInstance(y, int)
        self.assertIsInstance(y, Int)
        self.assertEqual(y, 506)

    def test_none(self):
        z = Int(None)
        self.assertIsNone(z)


class StringTest(TestCase):
    def test_class_types(self):
        x = String("What is this?")
        self.assertIsInstance(x, str)
        self.assertIsInstance(x, String)
        self.assertEqual(x, "What is this?")

    def test_none(self):
        self.assertIsNone(String(None))


class FloatTest(TestCase):
    def test_class_types(self):
        x = Float(2.84)
        self.assertIsInstance(x, float)
        self.assertIsInstance(x, Float)
        self.assertEqual(x + 1, 3.84)


class BooleanTest(TestCase):
    def test_class_types(self):
        self.assertTrue(Boolean(True))
        self.assertFalse(Boolean(False))
        self.assertEqual(typedef(Boolean).name, "Boolean")

    def test_none(self):
        self.assertIsNone(Boolean(None))


class IDTest(TestCase):
    def test_id_string(self):
        x = ID("123-456")
        self.assertEqual(x, "123-456")

    def test_id_int(self):
        y = ID(7890)
        self.assertEqual(y, "7890")
