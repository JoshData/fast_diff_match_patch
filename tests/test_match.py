from __future__ import unicode_literals

import unittest
import sys

import diff_match_patch

if sys.version_info[0] == 3:
    diff = diff_match_patch.diff
    diff_bytes = diff_match_patch.diff_bytes
    match_main = diff_match_patch.match_main
    match_main_bytes = diff_match_patch.match_main_bytes
else:
    diff = diff_match_patch.diff_unicode
    diff_bytes = diff_match_patch.diff_str
    match_main = diff_match_patch.match_main_unicode
    match_main_bytes = diff_match_patch.match_main_str


class MatchTests(unittest.TestCase):
    def test_unicode(self):
        self.assertEqual(0, match_main('abcdef', 'abcdef', 1000))

        self.assertEqual(-1, match_main('', 'abcdef', 1))

        self.assertEqual(3, match_main('abcdef', '', 3))

        self.assertEqual(3, match_main('abcdef', 'de', 3))

        self.assertEqual(3, match_main('abcdef', 'defy', 4))

        self.assertEqual(0, match_main('abcdef', 'abcdefy', 0))

        self.assertEqual(2, match_main('abc\u2192def', 'c\u2192defy', 0))

    def test_bytes(self):
        self.assertEqual(0, match_main_bytes(b'abcdef', b'abcdef', 1000))

        self.assertEqual(-1, match_main_bytes(b'', b'abcdef', 1))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'', 3))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'de', 3))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'defy', 4))

        self.assertEqual(0, match_main_bytes(b'abcdef', b'abcdefy', 0))

        self.assertEqual(2, match_main_bytes(b'abc\xe2\x86\x92def', b'c\xe2\x86\x92defy', 0))
