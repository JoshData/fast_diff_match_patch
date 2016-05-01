import sys
import diff_match_patch

if sys.version_info[0] == 3:
	diff = diff_match_patch.diff
	diff_bytes = diff_match_patch.diff_bytes
else:
	diff = diff_match_patch.diff_unicode
	diff_bytes = diff_match_patch.diff_str

def test(text1, text2, diff_function):
	print(diff_function.__name__)
	print("-" * len(diff_function.__name__))
	print ("<", repr(text1))
	print (">", repr(text2))
	print()

	print (diff_function(text1, text2, checklines=False, cleanup_semantic=True, as_patch=True))
	print()

	changes = diff_function(
		text1, text2,
		timelimit=15,
		checklines=False,
		cleanup_semantic=True,
		counts_only=False)

	for op, text in changes:
		print(op, repr(text))

	print ("")

	changes = diff_function(
		text1, text2,
		timelimit=15,
		checklines=False,
		cleanup_semantic=True,
		counts_only=True)

	t1pos, t2pos = 0, 0
	for op, length in changes:
		if op == '=':
			text = text1[t1pos:t1pos + length]
			t1pos += length
			t2pos += length
		elif op == '+':
			text = text2[t2pos:t2pos + length]
			t2pos += length
		elif op == '-':
			text = text1[t1pos:t1pos + length]
			t1pos += length
		print(op, repr(text))

	print ("")

test(u"this is a test", u"this program is not \u2192 a test", diff)
test(u"\U0001f37e", u"\U0001f37f", diff)  # surrogate pair in UTF-16
test(b"this is a test", b"this program is not ==> a test", diff_bytes)
	
