from __future__ import unicode_literals

import sys
import unittest

import fast_diff_match_patch

class DiffTests(unittest.TestCase):
    def assertDiff(self, text1, text2, expected):
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
        self.assertEqual(actual, [(op, len(text)) for (op, text) in expected])

    def test_string(self):
        self.assertDiff(
            '',
            '',
            []
        )

        self.assertDiff(
            'this is a test',
            'this is a test',
            [('=', 'this is a test')]
        )

        self.assertDiff(
            'this is a test',
            'this program is not \u2192 a test',
            [
                ('=', 'this '),
                ('-', 'is'),
                ('+', 'program is not \u2192'),
                ('=', ' a test'),
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
            ]
        )

    def test_binary(self):
        self.assertDiff(
            b'',
            b'',
            []
        )

        self.assertDiff(
            b'this is a test',
            b'this is a test',
            [('=', b'this is a test')]
        )

        self.assertDiff(
            b'this is a test',
            b'this program is not ==> a test',
            [
                ('=', b'this '),
                ('-', b'is'),
                ('+', b'program is not ==>'),
                ('=', b' a test'),
            ]
        )

    def test_binary_safe(self):
        self.assertDiff(
            '1\u00002',
            '1\u00003',
            [('=', '1\x00'), ('-', '2'), ('+', '3')]
        )

        self.assertDiff(
            b'1\0002',
            b'1\0003',
            [('=', b'1\x00'), ('-', b'2'), ('+', b'3')]
        )

    def test_unicode_surrogate_pair(self):
        self.assertEqual(fast_diff_match_patch.CHAR_WIDTH, 4)

        self.assertDiff(
            '\U0001f37e',
            '\U0001f37f',
            [
                ('-', u'\U0001f37e'),
                ('+', u'\U0001f37f')
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

    def test_example_text_1(self):
        text1 = """diff_match_patch-python

A Python extension module that wraps google-diff-match-patch's C++ implementation for performing very fast string comparisons.

google-diff-match-patch is a Google library for computing differences between text files (<http://code.google.com/p/google-diff-match-patch>). Thare are implementations in various languages. Although there is a Python port, it's slow on very large documents, and I have a need for speed. I wanted to use the C++ implementation, but I'm a Python guy so I'd prefer to use it from Python.

@leutloff determined that the C++ port could be even faster by replacing the Qt 4 dependency with the standard C++ library primitives. So he rewrote the module at <https://github.com/leutloff/diff-match-patch-cpp-stl>.

This project is an extension module for Python using @leutloff's library so Python code can call into the native library easily. It works in both Python 2 and Python 3."""

        text2 = """fast\_diff\_match\_patch: Python package wrapping the C++ implementation of google-diff-match-patch
===================================================================================================

This is a Python 3.6+ package that wraps google-diff-match-patch\'s C++
implementation for performing very fast string comparisons. This package
was previously known as diff\_match\_patch\_python.

google-diff-match-patch is a Google library for computing differences
between text files (http://code.google.com/p/google-diff-match-patch).
There are implementations in various languages. Although there is a Python
port, it's slow on very large documents, and I have a need for speed. I
wanted to use the C++ implementation, but I'm a Python guy so I'd
prefer to use it from Python.

Google's library depends on Qt 4, so some other folks rewrote it using
the standard C++ library classes instead, making it more portable.
That's at https://github.com/leutloff/diff-match-patch-cpp-stl. This
package uses that library."""

        actual = fast_diff_match_patch.diff(text1, text2)
        
        self.assertEqual(actual,
                         [('+', 6), ('=', 4), ('+', 1), ('=', 6), ('+', 1),
                          ('=', 6), ('-', 2), ('+', 3), ('=', 5), ('-', 26),
                          ('+', 197), ('=', 42), ('-', 1), ('+', 1), ('=', 59),
                          ('+', 65), ('=', 71), ('-', 1), ('+', 1), ('=', 20),
                          ('-', 1), ('=', 48), ('-', 1), ('=', 2), ('-', 1),
                          ('+', 1), ('=', 2), ('-', 1), ('+', 1), ('=', 71),
                          ('-', 1), ('+', 1), ('=', 71), ('-', 1), ('+', 1),
                          ('=', 65), ('-', 1), ('+', 1), ('=', 31), ('-', 159),
                          ('+', 144), ('=', 4), ('-', 1), ('=', 52), ('-', 171),
                          ('+', 32), ('=', 1)])

        actual = fast_diff_match_patch.diff(text1, text2, as_patch=True)

        self.assertEqual(actual, """@@ -1,53 +1,233 @@
+fast%5C_
 diff
+%5C
 _match
+%5C
 _patch
--p
+: P
 ython
-%0A%0AA Python extension modul
+ package wrapping the C++ implementation of google-diff-match-patch%0A===================================================================================================%0A%0AThis is a Python 3.6+ packag
 e th
@@ -260,25 +260,25 @@
 -patch's C++
- 
+%0A
 implementati
@@ -324,16 +324,81 @@
 arisons.
+ This package%0Awas previously known as diff%5C_match%5C_patch%5C_python.
 %0A%0Agoogle
@@ -460,17 +460,17 @@
 ferences
- 
+%0A
 between 
@@ -481,17 +481,16 @@
  files (
-%3C
 http://c
@@ -533,15 +533,14 @@
 atch
-%3E
 ).
- 
+%0A
 Th
-a
+e
 re a
@@ -606,17 +606,17 @@
 a Python
- 
+%0A
 port, it
@@ -678,17 +678,17 @@
 speed. I
- 
+%0A
 wanted t
@@ -744,17 +744,17 @@
 y so I'd
- 
+%0A
 prefer t
@@ -780,172 +780,156 @@
 n.%0A%0A
-@leutloff determined that the C++ port could be even faster by replacing the Qt 4 dependency with the standard C++ library primitives. So he rewrote the module
+Google's library depends on Qt 4, so some other folks rewrote it using%0Athe standard C++ library classes instead, making it more portable.%0AThat's
  at 
-%3C
 http
@@ -980,176 +980,37 @@
 -stl
-%3E.%0A%0AThis project is an extension module for Python using @leutloff's library so Python code can call into the native library easily. It works in both Python 2 and Python 3
+. This%0Apackage uses that library
 .
""")

        pattern = """This is a Python 3.6+ package."""
        actual = fast_diff_match_patch.match(text2, pattern, loc=20)
        self.assertEqual(actual, 201)
