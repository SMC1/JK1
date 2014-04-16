#!/usr/bin/python

import os, re, sys
from glob import glob

def main(inDirN='/EQL3/pipeline/Clonality'):
	inFileNL = glob('%s/*/*mutect_cl.dat' % inDirN)

	for inFileN in inFileNL:
		(sampN,) = re.match('(.*).mutect_cl.dat', os.path.basename(inFileN)).groups()
		(sid, postfix) = re.match('(.*)_([BNTXC].{,2})_[KNST]{2}', sampN).groups()
		if postfix != 'T':
			sid = '%s_%s' % (sid, postfix)

		inFile = open(inFileN, 'r')
		for line in inFile:
			if 'REJECT' not in line:
				colL = line.rstrip().split('\t')
				chr = colL[0]
				pos = colL[1]
				ref = colL[2]
				alt = colL[3]
				if colL[8] != 'ND':
					clonality = int(float(colL[8]) * 100.0)
				else:
					clonality = colL[8]
				sys.stdout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sid, chr, pos,pos, ref, alt, clonality))

if __name__ == '__main__':
	main(inDirN='/EQL3/pipeline/Clonality')
