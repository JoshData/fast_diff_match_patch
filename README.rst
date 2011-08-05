diff_match_patch extension module for Python based on google-diff-match-patch
---

google-diff-match-patch is a Google library for computing differences between text files:

 http://code.google.com/p/google-diff-match-patch
 
This project builds an extension module for Python using google-diff-match-patch's C++ implementation.

Build:

 python setup.py install

Usage:

 import diff_match_patch
 
 left_text = "this is a test"
 right_text = "this is not a test"
 
 diff = diff_match_patch.diff(left_text, right_text)
 
 for op, length in diff:
	if op == "-":
		print "next", length, "characters are deleted"
	if op == "=":
		print "next", length, "characters are in common"
	if op == "+":
		print "next", length, "characters are inserted"


