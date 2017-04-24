from unittest import TestCase

from polygraph.types.api import get_type_class
from polygraph.types.lazy_type import LazyType
from polygraph.types.scalar import Int
from polygraph.types.tests.helper import Person


class APITest(TestCase):
    def test_get_type_class(self):
        self.assertEqual(
            get_type_class(LazyType("Person", "polygraph.types.tests.helper")),
            Person,
        )
        self.assertEqual(
            get_type_class(Int),
            Int,
        )
