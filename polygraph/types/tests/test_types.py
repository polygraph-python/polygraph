from unittest import TestCase

from polygraph.exceptions import PolygraphValueError
from polygraph.types.list import List
from polygraph.types.nonnull import NonNull
from polygraph.types.scalar import Int, String


class NonNullTest(TestCase):

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

    def test_square_bracket_notation(self):
        self.assertEqual(NonNull(String), NonNull[String])


class ListTest(TestCase):

    def test_scalar_list(self):
        int_list = List(Int)
        self.assertEqual(int_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(int_list(None), None)
        with self.assertRaises(ValueError):
            int_list(["a", "b", "c"])

    def test_list_of_nonnulls(self):
        string_list = List(NonNull(String))
        self.assertEqual(string_list(["a", "b", "c"]), ["a", "b", "c"])
        with self.assertRaises(PolygraphValueError):
            string_list(["a", "b", "c", None])

    def test_square_bracket_notation(self):
        self.assertEqual(List(Int), List[Int])
