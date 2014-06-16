import sys
import diff_match_patch

if sys.version_info[0] == 3:
	diff = diff_match_patch.diff
	diff_bytes = diff_match_patch.diff_bytes
else:
	diff = diff_match_patch.diff_unicode
	diff_bytes = diff_match_patch.diff_str

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
	
print ("============")

left_text = b"this is a test"
right_text = b"this is not-> a test"

changes = diff_bytes(left_text, right_text, timelimit=15, checklines=False)

for op, length in changes:
	if op == "-":
		print ("next", length, "bytes are deleted")
	if op == "=":
		print ("next", length, "bytes are in common")
	if op == "+":
		print ("next", length, "bytes are inserted")
