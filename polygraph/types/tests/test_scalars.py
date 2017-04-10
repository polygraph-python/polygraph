from unittest import TestCase
from polygraph.types.scalar import Int


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
