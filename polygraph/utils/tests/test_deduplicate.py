from polygraph.utils.deduplicate import deduplicate
from unittest import TestCase


class DeduplicateTest(TestCase):
    def test_deduplicate(self):
        args = ['d', 'e', 'd', 'u', 'p', 'l', 'i', 'c', 'a', 't', 'e']
        self.assertEqual(
            list(deduplicate(args)),
            ['d', 'e', 'u', 'p', 'l', 'i', 'c', 'a', 't'],
        )
