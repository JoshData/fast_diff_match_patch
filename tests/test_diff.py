from __future__ import unicode_literals

import sys
import unittest

import diff_match_patch

if sys.version_info[0] == 3:
    diff = diff_match_patch.diff
    diff_bytes = diff_match_patch.diff_bytes
else:
    diff = diff_match_patch.diff_unicode
    diff_bytes = diff_match_patch.diff_str


class DiffTests(unittest.TestCase):
    def assertDiffString(self, text1, text2, expected, expected_counts_only):
        actual = diff(
            text1, text2,
            timelimit=15,
            checklines=False,
            cleanup_semantic=True,
            counts_only=False)
        self.assertEqual(actual, expected)

        actual = diff(
            text1, text2,
            timelimit=15,
            checklines=False,
            cleanup_semantic=True,
            counts_only=True)
        self.assertEqual(actual, expected_counts_only)

    def assertDiffBytes(self, text1, text2, expected, expected_counts_only):
        actual = diff_bytes(
            text1, text2,
            timelimit=15,
            checklines=False,
            cleanup_semantic=True,
            counts_only=False)
        self.assertEqual(actual, expected)

        actual = diff_bytes(
            text1, text2,
            timelimit=15,
            checklines=False,
            cleanup_semantic=True,
            counts_only=True)
        self.assertEqual(actual, expected_counts_only)

    def test_string(self):
        self.assertDiffString(
            '',
            '',
            [],
            [],
        )

        self.assertDiffString(
            'this is a test',
            'this is a test',
            [('=', 'this is a test')],
            [('=', 14)],
        )

        self.assertDiffString(
            'this is a test',
            'this program is not \u2192 a test',
            [
                ('=', 'this '),
                ('-', 'is'),
                ('+', 'program is not \u2192'),
                ('=', ' a test'),
            ],
            [
                ('=', 5),
                ('-', 2),
                ('+', 16),
                ('=', 7),
            ]
        )

    def test_diff_bytes(self):
        self.assertDiffBytes(
            b'',
            b'',
            [],
            [],
        )

        self.assertDiffBytes(
            b'this is a test',
            b'this is a test',
            [('=', 'this is a test')],
            [('=', 14)],
        )

        self.assertDiffBytes(
            b'this is a test',
            b'this program is not ==> a test',
            [
                ('=', 'this '),
                ('-', 'is'),
                ('+', 'program is not ==>'),
                ('=', ' a test'),
            ],
            [
                ('=', 5),
                ('-', 2),
                ('+', 18),
                ('=', 7),
            ]
        )

    def test_unicode_surrogate_pair(self):
        self.assertDiffString(
            '\U0001f37e',
            '\U0001f37f',
            [
                ('-', u'\U0001f37e'),
                ('+', u'\U0001f37f')
            ],
            [
                ('-', 1),
                ('+', 1),
            ]
        )