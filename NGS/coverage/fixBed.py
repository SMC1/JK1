#!/usr/bin/python

import sys

for line in sys.stdin:
	if line[:3] != 'chr':
		sys.stdout.write('chr%s' % line)
