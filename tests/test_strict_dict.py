import pytest

from polygraph.utils.strict_dict import StrictDict


def test_cannot_update_same_key_with_different_value():
    d = StrictDict()
    d["George"] = "Washington"
    d["John"] = "Adams"
    with pytest.raises(ValueError):
        d["George"] = "Bush"
    assert d["George"] == "Washington"


def test_can_update_same_key_with_same_value():
    d = StrictDict()
    d["George"] = "Bush"
    d["Bill"] = "Clinton"
    d["George"] = "Bush"
    assert d["George"] == "Bush"
