diff_match_patch-python
=======================

A Python extension module that wraps google-diff-match-patch's C++ implementation for performing very fast string comparisons.

google-diff-match-patch is a Google library for computing differences between text files (<http://code.google.com/p/google-diff-match-patch>). Thare are implementations in various languages. Although there is a Python port, it's slow on very large documents, and I have a need for speed. I wanted to use the C++ implementation, but I'm a Python guy so I'd prefer to use it from Python.

@leutloff determined that the C++ port could be even faster by replacing the Qt 4 dependency with the standard C++ library primitives. So he rewrote the module at <https://github.com/leutloff/diff-match-patch-cpp-stl>.
 
This project is an extension module for Python using @leutloff's library so Python code
can call into the native library easily. It works in both Python 2 and Python 3.

Example
-------

First::

	pip3 install diff_match_patch_python

Then write (this is Python 3)::

	from diff_match_patch import diff

	changes = diff("Hello world.", "Goodbye moon.",
		timelimit=0, checklines=False)

	for op, length in changes:
		if op == "-": print ("next", length, "characters are deleted")
		if op == "=": print ("next", length, "characters are in common")
		if op == "+": print ("next", length, "characters are inserted")

The module also provides a method called ``diff_bytes`` for performing a diff on a bytes array.

In Python 2, the methods are named ``diff_unicode`` (unicode strings) and ``diff_str`` (str strings).

The ``timelimit`` argument is the maximum running time in seconds if you want to ensure the result comes quickly. According to the Google docs, the diff will stop working after the time is exceeded and will return a valid diff, but it might not be the best one. ``checklines`` is also a Google thing and might speed up diffs that are over lined-based text like code.

The diff methods also take a ``counts_only`` argument which is ``True`` by default. Set it to ``False`` to have the returned value be an array of tuples of operations and corresponding strings rather than operations and the lengths of those strings.

Dependencies
------------

To build from source, you will need:

* Python development headers (Debian package ``python-dev``)
* The diff-match-patch library, which you can clone using ``git submodule update --init``.
 		
Build
-----

Build the binary module using::

 python setup.py install
 
Or you may find pre-built binaries stored in the git repository in the build directory.
Your mileage may vary with these depending on whether your system is compatible.


