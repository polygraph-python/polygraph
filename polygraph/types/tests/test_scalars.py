from unittest import TestCase

from polygraph.types.scalar import Boolean, Float, Int, String


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


class StringTest(TestCase):
    def test_class_types(self):
        x = String("What is this?")
        self.assertIsInstance(x, str)
        self.assertIsInstance(x, String)
        self.assertEqual(x, "What is this?")


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
        self.assertEqual(Boolean(True)._type.name, "Boolean")
