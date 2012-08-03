#!/usr/bin/python

import sys, os

i = 0

for line in open(sys.argv[1]):

	if line[0] == '#' or line[:15] == 'AlignmentBlocks':
		continue

	i += 1

print 'Mapped_reads\t%s' % i
