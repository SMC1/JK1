#!/usr/bin/python

import sys, getopt, re
import mybasic


def main():

	for line in sys.stdin:

		chrom = line.split(':')[0]
		tail = line[:-1].split(':')[1].split('-')

		if len(tail) == 1:
			chrSta = chrEnd = int(tail[0])
		else:
			chrSta = int(tail[0])
			chrEnd = int(tail[1])

		sys.stdout.write('%s\t%s\t%s\n' % (chrom,chrSta-1,chrEnd))


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])
#optH = mybasic.parseParam(optL)

main()
