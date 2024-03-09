from __future__ import unicode_literals

import unittest
import sys

from fast_diff_match_patch import match

class MatchTests(unittest.TestCase):
    def test_unicode(self):
        self.assertEqual(0, match('abcdef', 'abcdef', 1000))

        self.assertEqual(-1, match('', 'abcdef', 1))

        self.assertEqual(3, match('abcdef', '', 3))

        self.assertEqual(3, match('abcdef', 'de', 3))

        self.assertEqual(3, match('abcdef', 'defy', 4))

        self.assertEqual(0, match('abcdef', 'abcdefy', 0))

        self.assertEqual(2, match('abc\u2192def', 'c\u2192defy', 0))

    def test_bytes(self):
        self.assertEqual(0, match(b'abcdef', b'abcdef', 1000))

        self.assertEqual(-1, match(b'', b'abcdef', 1))

        self.assertEqual(3, match(b'abcdef', b'', 3))

        self.assertEqual(3, match(b'abcdef', b'de', 3))

        self.assertEqual(3, match(b'abcdef', b'defy', 4))

        self.assertEqual(0, match(b'abcdef', b'abcdefy', 0))

        self.assertEqual(2, match(b'abc\xe2\x86\x92def', b'c\xe2\x86\x92defy', 0))
