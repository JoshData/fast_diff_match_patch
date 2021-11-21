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

    def test_binary(self):
        self.assertDiff(
            b'',
            b'',
            [],
            [],
        )

        self.assertDiff(
            b'this is a test',
            b'this is a test',
            [('=', b'this is a test')],
            [('=', 14)],
        )

        self.assertDiff(
            b'this is a test',
            b'this program is not ==> a test',
            [
                ('=', b'this '),
                ('-', b'is'),
                ('+', b'program is not ==>'),
                ('=', b' a test'),
            ],
            [
                ('=', 5),
                ('-', 2),
                ('+', 18),
                ('=', 7),
            ]
        )

    def test_binary_safe(self):
        self.assertDiff(
            '1\u00002',
            '1\u00003',
            [('=', '1\x00'), ('-', '2'), ('+', '3')],
            [('=', 2), ('-', 1), ('+', 1)],
        )

        self.assertDiff(
            b'1\0002',
            b'1\0003',
            [('=', b'1\x00'), ('-', b'2'), ('+', b'3')],
            [('=', 2), ('-', 1), ('+', 1)],
        )

    @unittest.skipIf(fast_diff_match_patch.CHAR_WIDTH != 4,
                     "not supported on this platform") # strings become '\ud83c\udf7e' and '\ud83c\udf7f' on Windows
    def test_unicode_surrogate_pair(self):
        self.assertEqual(fast_diff_match_patch.CHAR_WIDTH, 4)

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

    # on Windows only
    @unittest.skipIf(fast_diff_match_patch.CHAR_WIDTH == 4,
                     "does nothing on this platform")
    def test_unicode_surrogate_pair_detected(self):
        self.assertEqual(fast_diff_match_patch.CHAR_WIDTH, 2)
        self.assertRaises(RuntimeError, lambda : fast_diff_match_patch.diff('\U0001f37e', '\U0001f37f'))

    def test_patch(self):
        actual = fast_diff_match_patch.diff(
            "Text 1",
            "Text 2",
            as_patch=True)
        self.assertEqual(actual, """@@ -2,5 +2,5 @@
 ext 
-1
+2
""")
