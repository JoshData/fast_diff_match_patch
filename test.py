import diff_match_patch

left_text = "this is a test"
right_text = "this is not a test"

diff = diff_match_patch.diff(left_text, right_text, timelimit=15)

for op, length in diff:
	if op == "-":
		print "next", length, "characters are deleted"
	if op == "=":
		print "next", length, "characters are in common"
	if op == "+":
		print "next", length, "characters are inserted"
	

