fast\_diff\_match\_patch: Python package wrapping the C++ implementation of google-diff-match-patch
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
package uses that library.

(This package can hopefully still be built for Python 2.7 also but a
pre-built package is not available.)

Example
-------

First:

    pip3 install fast_diff_match_patch

Then write (this is Python 3):

    from fast_diff_match_patch import diff

    changes = diff("Hello world.", "Goodbye moon.")

    for op, length in changes:
        if op == "-": print ("next", length, "characters are deleted")
        if op == "=": print ("next", length, "characters are in common")
        if op == "+": print ("next", length, "characters are inserted")

The two textual arguments can be either strings or bytes (Unicode or str on Python 2.x).

Some keyword arguments are also available:

`timelimit` (default 0) gives the maximum running time in seconds if you
want to ensure the result comes quickly. According to the Google docs,
the diff will stop working after the time is exceeded and will return a
valid diff, but it might not be the best one. `checklines` is also a
Google thing and might speed up diffs that are over lined-based text
like code.

`checklines` (default `True`) is the same argument in the diff_main
subroutine of the main library.

`cleanup` (default `"Semantic"`) is `"Semantic"`, `"Efficiency"`, or `"No"`
to run the corresponding cleanup subroutine after performing the diff.

Set `counts_only` (default `True`) to `False` to have the returned value be an array of
tuples of operations and corresponding strings rather than operations
and the lengths of those strings.

If `as_patch` (default `False`) is `True`, the diff is returned in patch format
as a string.

On Windows, an exception will be thrown if either of the two text strings has characters
outside of the Basic Multilingual Plane because the native platform character type
is a two-byte character. The `fast_diff_match_patch.CHAR_WIDTH` field, which will either
be 2 or 4, can be used to determine whether these characters are supported ahead of time.

The Global Interpreter Lock (GIL) is released while performing the diff
so that this library can be used in a multi-threaded application.


Changelog
---------

### Version 2.0.1

* Diffs of byte strings are now null-character-safe.
* Fixed `as_patch` argument.

### Version 2.0.0

* The import has been renamed from `diff_match_patch` to `fast_diff_match_patch` to avoid an import naming collision with https://pypi.org/project/diff-match-patch/ and the package name has been updated to match the import name.
* In previous versions of this package, separate `diff_bytes` (Py3), `diff_unicode` and `diff_str` (Py2)
methods were available. They have been merged into a single `diff` method that checks the type of the arguments passed.)
* `cleanup_semantic` has been renamed to `cleanup`, which takes one of three options (see above)
* On Windows, an exception will be thrown if a string has characters outside of the Basic Multilingual Plane.

Building from source
--------------------

To build from these sources, you will need:

-   Python development headers and the setuptools package
    (Debian packages `python3-dev`, `python3-setuptools`)
-   The diff-match-patch library, which you can clone using
    `git submodule update --init`.

Then build/install the binary module using:

    python setup.py build
    python setup.py install


For package maintainers
-----------------------

To build everything (for testing):

    git submodule update && rm -rf build && python3 setup.py build

To test without installing:

    PYTHONPATH=build/lib.linux-x86_64-*/ python3 -m unittest

To upload a new release to PyPi:

* Install twine: `python3 -m pip install --upgrade twine`
* manylinux wheels are built automatically on GitHub Actions.
* Download the artifact and extract the files to a new directory.
* Upload them: `python3 -m twine upload path-to-artifact-files/*`. Username: `__token__`; Password: A PyPi API token.

