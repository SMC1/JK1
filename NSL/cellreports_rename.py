#!/usr/bin/python

import sys, os

baseDir = '/data1/IRCR/array_201111'

samples = [line.rstrip()[-3:] for line in open('cellreports_samples.txt')]

for s in samples:

	print '%s: ' % s,

	ll_result = os.popen('ls -l %s/*%s*' % (baseDir,s)).readlines()

	if 'cannot' in ll_result[0]:
		print '[]'
		continue

	if len(ll_result) > 1:
		print ll_result
		continue

	os.system('cp %s %s/Joo_et_al/S%s.CEL' % (ll_result[0].rstrip().split(' ')[-1], baseDir,s))
	print 'OK'
