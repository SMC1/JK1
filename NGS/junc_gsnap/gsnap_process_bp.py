#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


#def fastaCoord(fastaFileName):
#
#	tokL = open(fastaFileName).readline().split(' ')
#
#	rm = re.match('range=([^:]+):([0-9]+)-([0-9]+)',tokL[1])
#	chrom, chrSta, chrEnd = rm.groups()
#
#	rm = re.match('strand=([+-])',tokL[4])
#	strand = rm.group(1)
#
#	return (chrom, chrSta, chrEnd, strand)
	

def process_bp(inGsnapFileName):

	result = mygsnap.gsnapFile(inGsnapFileName,False)
	#outBpFile = open(outBpFileName, 'w')

	seqH = {}

	for r in result:

		match = r.matchL()[0]

		if not '(transloc)' in r.pairRel:
			raise Exception

		if len(match.segL) != 2:
			raise Exception

		s1 = match.segL[0][2]
		s2 = match.segL[1][2]

		if s1[0] != s2[0]:
			raise Exception

		strand = s1[0]

		bp1 = re.match('[+-]([^:]+):[0-9]+..([0-9]+)',s1).groups()
		bp2 = re.match('[+-]([^:]+):([0-9]+)..[0-9]+',s2).groups()

		if strand == '+':
			seq = r.seq()
			offset = int(match.segL[0][1].split('..')[1])
			bp12 = (bp1, bp2)
		else:
			seq = mybasic.rc(r.seq(),'DNA')
			offset = len(seq)-int(match.segL[0][1].split('..')[1])
			bp12 = (bp2, bp1)

		mybasic.addHash(seqH,bp12,(offset,seq))

	seqL = seqH.items()
	seqL.sort(lambda x,y: cmp(len(y[1]),len(x[1])))

	for ((bp1,bp2), vL) in seqL:

		vL.sort(lambda x,y: cmp(y[0],x[0]))

		maxOffset = vL[0][0]

		print '\n',bp1,bp2,len(vL),'\n'

		for (offset,seq) in vL:

			print '%s%s %s' % (' ' * (maxOffset-offset),seq[:offset],seq[offset:])

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	process_bp(optH['-i'])

#process_bp('test.gsnap','test.bp')
