#!/usr/bin/python

import os

for chr in (range(1,20)+['X','Y','M']):

	os.system('xdformat -n -o chr%s.fa /nfs/genomes/mouse_gp_jul_07/chr%s.fa' % (`chr`,`chr`,))
