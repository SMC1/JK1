#!/usr/bin/python

import sys, os

for cmd in sys.stdin:

	os.system('echo "%s" | qsub -l walltime=99:99:99:99' % (cmd,))
