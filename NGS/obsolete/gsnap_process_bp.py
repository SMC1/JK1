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

	for ((k1,k2), v) in seqH.items():

		v.sort(lambda x,y: cmp(y[0],x[0]))

		k1T = re.match()
		k2T = re.match()

		k1_pos = 
		k2_pos = 

		k1_seq = 
		k2_seq = 

		outBpFile.write('%s,%s,%s\n' % (':'.join(k1),':'.join(k2),'|'.join(['%s:%s' % (offset,seq) for (offset,seq) in v])))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	process_bp(optH['-i'], optH['-o'])

process_bp('test.gsnap','test.bp')
