import diff_match_patch

left_text = u"this is a test"
right_text = u"this is not \u2192 a test"

diff = diff_match_patch.diff_unicode(left_text, right_text, timelimit=15, checklines=False)

for op, length in diff:
	if op == "-":
		print "next", length, "characters are deleted"
	if op == "=":
		print "next", length, "characters are in common"
	if op == "+":
		print "next", length, "characters are inserted"
	
print "============"

left_text = "this is a test"
right_text = "this is not-> a test"

diff = diff_match_patch.diff_str(left_text, right_text, timelimit=15, checklines=False)

for op, length in diff:
	if op == "-":
		print "next", length, "bytes are deleted"
	if op == "=":
		print "next", length, "bytes are in common"
	if op == "+":
		print "next", length, "bytes are inserted"
