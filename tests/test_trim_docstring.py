from polygraph.utils.trim_docstring import trim_docstring


class WellDocumentedObject(object):
    """
    This object is very well-documented. It has multiple lines in its
    description.

    Multiple paragraphs too
    """
    pass


class UndocumentedObject(object):
    pass


def test_trim_docstring():
    assert trim_docstring(WellDocumentedObject.__doc__) == (
        "This object is very well-documented. It has multiple lines "
        "in its\ndescription.\n\nMultiple paragraphs too"
    )


def test_trim_empty_docstring_returns_none():
    assert trim_docstring(UndocumentedObject.__doc__) is None
