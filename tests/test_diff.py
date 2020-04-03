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
            [('0', 'this is a test')],
            [('0', 14)],
        )

        self.assertDiffString(
            'this is a test',
            'this program is not \u2192 a test',
            [
                ('0', 'this '),
                ('-1', 'is'),
                ('1', 'program is not \u2192'),
                ('0', ' a test'),
            ],
            [
                ('0', 5),
                ('-1', 2),
                ('1', 16),
                ('0', 7),
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
            [('0', 'this is a test')],
            [('0', 14)],
        )

        self.assertDiffBytes(
            b'this is a test',
            b'this program is not ==> a test',
            [
                ('0', 'this '),
                ('-1', 'is'),
                ('1', 'program is not ==>'),
                ('0', ' a test'),
            ],
            [
                ('0', 5),
                ('-1', 2),
                ('1', 18),
                ('0', 7),
            ]
        )

    def test_unicode_surrogate_pair(self):
        self.assertDiffString(
            '\U0001f37e',
            '\U0001f37f',
            [
                ('-1', u'\U0001f37e'),
                ('1', u'\U0001f37f')
            ],
            [
                ('-1', 1),
                ('1', 1),
            ]
        )
