import sys
import diff_match_patch

if sys.version_info[0] == 3:
	diff = diff_match_patch.diff
else:
	diff = diff_match_patch.diff_unicode

left_text = u"this is a test"
right_text = u"this is not \u2192 a test"

changes = diff(left_text, right_text, timelimit=15, checklines=False)

for op, length in changes:
	if op == "-":
		print ("next", length, "characters are deleted")
	if op == "=":
		print ("next", length, "characters are in common")
	if op == "+":
		print ("next", length, "characters are inserted")
	
if sys.version_info[0] == 2:
	# Byte-by-byte comparison for Python 2 only.

	print ("============")

	left_text = "this is a test"
	right_text = "this is not-> a test"

	changes = diff_match_patch.diff_str(left_text, right_text, timelimit=15, checklines=False)

	for op, length in changes:
		if op == "-":
			print ("next", length, "bytes are deleted")
		if op == "=":
			print ("next", length, "bytes are in common")
		if op == "+":
			print ("next", length, "bytes are inserted")
