#!/usr/bin/python

import sys
import re

sys.stdout.write(sys.stdin.readline())

for line in sys.stdin:

	line = line.replace('mutation_normal','Exome-Seq').replace('mutation_rsq','RNA-Seq')
	sys.stdout.write(re.sub('S([0-9]{3})-S([0-9]{3})',lambda mo: '%sT-%sT' % (mo.group(1),mo.group(2)),line))
