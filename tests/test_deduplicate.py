from polygraph.utils.deduplicate import deduplicate


def test_deduplicate():
    args = ['d', 'e', 'd', 'u', 'p', 'l', 'i', 'c', 'a', 't', 'e']
    assert list(deduplicate(args)) == ['d', 'e', 'u', 'p', 'l', 'i', 'c', 'a', 't']
