from unittest import TestCase

from polygraph.types.field import field
from polygraph.types.lazy_type import LazyType
from polygraph.types.object_type import ObjectType
from polygraph.types.tests.helper import Person


class SelfReferentialObject(ObjectType):
    """
    This is a test object
    """
    @field
    def selfie(self) -> LazyType("SelfReferentialObject"):
        return None

    @field
    def bestie(self) -> LazyType("Person", module_name="polygraph.types.tests.helper"):
        return None


class LazyTypeTest(TestCase):
    def test_lazy_type(self):
        self.assertEqual(
            LazyType("SelfReferentialObject").resolve_type(),
            SelfReferentialObject
        )
        self.assertEqual(
            LazyType("Person", module_name="polygraph.types.tests.helper").resolve_type(),
            Person,
        )

    def test_lazy_type_callable(self):
        self.assertIsInstance(
            SelfReferentialObject().selfie(),
            SelfReferentialObject
        )
        self.assertIsInstance(
            SelfReferentialObject().bestie(),
            Person,
        )
