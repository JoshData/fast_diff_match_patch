from __future__ import unicode_literals

import sys
import unittest

import fast_diff_match_patch

class DiffTests(unittest.TestCase):
    def assertDiff(self, text1, text2, expected, expected_counts_only):
        actual = fast_diff_match_patch.diff(
            text1, text2,
            timelimit=15,
            checklines=False,
            counts_only=False)
        self.assertEqual(actual, expected)

        actual = fast_diff_match_patch.diff(
            text1, text2,
            timelimit=15,
            checklines=False)
        self.assertEqual(actual, expected_counts_only)

    def test_string(self):
        self.assertDiff(
            '',
            '',
            [],
            [],
        )

        self.assertDiff(
            'this is a test',
            'this is a test',
            [('=', 'this is a test')],
            [('=', 14)],
        )

        self.assertDiff(
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

    def test_diff(self):
        self.assertDiff(
            b'',
            b'',
            [],
            [],
        )

        self.assertDiff(
            b'this is a test',
            b'this is a test',
            [('=', 'this is a test')],
            [('=', 14)],
        )

        self.assertDiff(
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
        self.assertDiff(
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
