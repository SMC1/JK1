#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


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

		direction = re.search('dir:([^,\t]*)', match.segL[0][3]).group(1)

		bp1 = re.match('[+-]([^:]+):[0-9]+..([0-9]+)',s1).groups()
		bp2 = re.match('[+-]([^:]+):([0-9]+)..[0-9]+',s2).groups()

#		if bp1[0] == bp2[0]:
#			continue

		if direction == 'sense':
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

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	process_bp(optH['-i'])

#process_bp('test.gsnap','test.bp')
