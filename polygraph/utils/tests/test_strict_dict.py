from unittest import TestCase

from polygraph.utils.strict_dict import StrictDict


class StrictDictTest(TestCase):
    def test_cannot_update_same_key_with_different_value(self):
        d = StrictDict()
        d["George"] = "Washington"
        d["John"] = "Adams"
        with self.assertRaises(ValueError):
            d["George"] = "Bush"
        self.assertEqual(d["George"], "Washington")

    def test_can_update_same_key_with_same_value(self):
        d = StrictDict()
        d["George"] = "Bush"
        d["Bill"] = "Clinton"
        d["George"] = "Bush"
        self.assertEqual(d["George"], "Bush")
