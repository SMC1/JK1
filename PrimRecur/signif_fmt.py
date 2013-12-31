#!/usr/bin/python

import sys
import re

sys.stdout.write(sys.stdin.readline())

for line in sys.stdin:

	line = line.replace('mutation_normal','Exome-Seq').replace('mutation_rsq','RNA-Seq')
	line = re.sub('S([0-9]{1})([ABC]{1})', lambda mo: 'S0%s' % mo.group(1), line)
	line = re.sub('S([0-9]{2})([ABC]{1})', lambda mo: 'S%s' % mo.group(1), line)
	line = re.sub('S([0-9]{3})', lambda mo: '%s' % mo.group(1), line)
	sys.stdout.write(re.sub('([0-9]{3}|S[0-9]{2})-([0-9]{3}|S[0-9]{2})',lambda mo: '%sP-%sR' % (mo.group(1),mo.group(2)),line))
