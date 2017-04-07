from ..trim_docstring import trim_docstring
from unittest import TestCase


class WellDocumentedObject(object):
    """
    This object is very well-documented. It has multiple lines in its
    description.

    Multiple paragraphs too
    """
    pass


class UndocumentedObject(object):
    pass


class TrimDocstringTest(TestCase):
    def test_trim_docstring(self):
        self.assertEqual(
            trim_docstring(WellDocumentedObject.__doc__),
            "This object is very well-documented. It has multiple lines "
            "in its\ndescription.\n\nMultiple paragraphs too"
        )

    def test_trim_empty_docstring_returns_none(self):
        self.assertIsNone(trim_docstring(UndocumentedObject.__doc__))
