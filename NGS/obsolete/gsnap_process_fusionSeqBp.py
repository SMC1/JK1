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
	

def process_bp(inGsnapFileName,outBpFileName):

	result = mygsnap.gsnapFile(inGsnapFileName,False)
	outBpFile = open(outBpFileName, 'w')

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

		s1T = re.match('[+-]([^:]+):[0-9]+..([0-9]+)',s1).groups()
		s2T = re.match('[+-]([^:]+):([0-9]+)..[0-9]+',s2).groups()

		if strand == '+':
			seq = r.seq()
			offset = int(match.segL[0][1].split('..')[1])
			junction = (s1T, s2T)
		else:
			seq = mybasic.rc(r.seq(),'DNA')
			offset = len(seq)-int(match.segL[0][1].split('..')[1])
			junction = (s2T, s1T)

		mybasic.addHash(seqH,junction,(offset,seq))

	for ((j1,j2), vL) in seqH.items():

		vL.sort(lambda x,y: cmp(x[0],y[0]))

		vL_mod = []

		for (offset,seq) in vL:

			offset = blockSize-offset+1
			vL_mod.append('%s:%s' % (offset,seq))

		outBpFile.write('%s:%s-%s,%s:%s-%s,%s\n' % (j1[0].split('_')[0],int(j1[1])-blockSize,j1[1], j1[0].split('_')[0],j1[1],int(j1[1])+blockSize, '|'.join(vL_mod)))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

blockSize = 100

if '-i' in optH and '-o' in optH:

	process_bp(optH['-i'], optH['-o'])

process_bp('test.gsnap','test.bp')
