diff_match_patch-python
=============================================================================

Python module based on google-diff-match-patch's C++ version as rewritten by @leutloff at
https://github.com/leutloff/diff-match-patch-cpp-stl which removes the Qt dependency.

So...

google-diff-match-patch is a Google library for computing differences between text files:

 http://code.google.com/p/google-diff-match-patch

Thare are implementations in various languages. Although there is a Python port, it's slow
on very large documents and I have a need for speed. So I wanted to use the C++ port. But
@leutloff determined that the C++ port could be even faster by replacing the Qt 4 dependency
with the standard C++ library primitives. So he rewrote the module:

 https://github.com/leutloff/diff-match-patch-cpp-stl to be faster
 
This project builds an extension module for Python using @leutloff's library so Python code
can call into the native library easily.

Dependencies
------------

You will need:

* Python development headers (Debian package `python-dev`)
* The diff-match-patch library, which you can clone using `git submodule update --init`.
 		
Build
-----

Build the binary module using::

 python setup.py install
 
Or you may find pre-built binaries stored in the git repository in the build directory.
Your mileage may vary with these depending on whether your system is compatible.

Example
-------

Example usage::

	import diff_match_patch

	left_text = u"this is a test"
	right_text = u"this is not a test"

	diff = diff_match_patch.diff_unicode(left_text, right_text)

	for op, length in diff:
	if op == "-":
		print "next", length, "characters are deleted"
	if op == "=":
		print "next", length, "characters are in common"
	if op == "+":
		print "next", length, "characters are inserted"

There is also a diff_str function that accepts str instances.

Options
-------

op_list = diff_match_patch.diff_{unicode,str}(left_text, right_text[, timelimit=0][, checklines=False][, counts_only=True])

left_text and right_text are strings (unicode or str as appropriate).

The optional timelimit specifies an upper bound on the amount of time
to compute the diff, in seconds, or zero (the default) to work on the
diff indefinitely. According to the Google docs, the diff will stop
working after the time is exceeded and will return a valid diff, but
it might not be the best one.

If checklines is True, the diff will do line-by-line comparisons first.

If counts_only is False, then instead of returning tuples of (op, length),
return tuples of (op, text) that gives the text needed to re-create
right_text from left_text.

