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

        self.assertDiff(
            'this\nis\na\ntest',
            'this\nprogram\nis\nnot \u2192 a\ntest',
            [
                ('=', 'this\n'),
                ('-', 'is\n'),
                ('+', 'program\nis\nnot \u2192 '),
                ('=', 'a\ntest'),
            ],
            [
                ('=', 5),
                ('-', 3),
                ('+', 17),
                ('=', 6),
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

        # Test that the byte string version also works although
        # it won't have any surrogate pair issues.
        self.assertDiff(
            '\U0001f37e'.encode("utf32"),
            '\U0001f37f'.encode("utf32"),
            [
                ('=', '\U0001f37e'.encode("utf32")[0:4]),
                ('-', '\U0001f37e'.encode("utf32")[4:5]),
                ('+', '\U0001f37f'.encode("utf32")[4:5]),
                ('=', '\U0001f37e'.encode("utf32")[5:8])
            ],
            [
                ('=', 4),
                ('-', 1),
                ('+', 1),
                ('=', 3)
            ]
        )

    def test_patch(self):
        actual = fast_diff_match_patch.diff(
            "Text 1\nLine 1\nLine 2\nLine 3",
            "Text 2\nLine 1\nLine 3\nLine 2",
            as_patch=True)
        self.assertEqual(actual, """@@ -1,14 +1,14 @@
 Text 
-1
+2
 %0ALine 1%0A
@@ -16,12 +16,12 @@
 ine 
-2
+3
 %0ALine 
-3
+2
""")


    def test_patch_binary(self):
        actual = fast_diff_match_patch.diff(
            b"Text 1\nLine 1\nLine 2\nLine 3",
            b"Text 2\nLine 1\nLine 3\nLine 2",
            as_patch=True)
        self.assertEqual(actual, b"""@@ -1,14 +1,14 @@
 Text 
-1
+2
 %0ALine 1%0A
@@ -16,12 +16,12 @@
 ine 
-2
+3
 %0ALine 
-3
+2
""")
