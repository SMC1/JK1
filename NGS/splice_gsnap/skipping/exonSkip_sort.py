#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def main(inGsnapFileName,outReportFileName,sampN):

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	juncHH = {}

	for r in result:

		if r.nLoci != 1:
			raise Exception

		match = r.matchL()[0]

		if len(match.segL) != 2:
			raise Exception

		direction = re.search('dir:([^,\t]*)', match.segL[0][3]).group(1)
		offset = int(re.search('\.\.([0-9]*)', match.segL[0][1]).group(1))

		exonLP = []

		for i in range(len(match.segL)):

			rm = re.search('label_[12]:([^,\t]*)',match.segL[i][3])

			if not rm:
				raise Exception

			exonLP.append(rm.group(1).replace('|',','))

		s1 = match.segL[0][2]
		s2 = match.segL[1][2]

		bp1 = re.match('([+-])([^:]+):[0-9]+..([0-9]+)',s1)
		bp2 = re.match('([+-])([^:]+):([0-9]+)..[0-9]+',s2)
			
		if (bp1.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand1 = '+'
		elif (bp1.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand1 = '-'
		else:
			raise Exception

		if (bp2.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand2 = '+'
		elif (bp2.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand2 = '-'
		else:
			raise Exception

		if direction=='sense':
			key = ((trans_strand1,)+bp1.groups()[1:],(trans_strand2,)+bp2.groups()[1:])

		elif direction=='antisense':
			key = ((trans_strand2,)+bp2.groups()[1:],(trans_strand1,)+bp1.groups()[1:])
			exonLP = exonLP[::-1]

		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'] += 1
			juncHH[key]['pos'].add((direction,offset))

		else:

			juncHH[key] = {'match':1, 'pos':set([(direction,offset)]), 'exonLP':exonLP}

	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['pos'])),len(set(x[1]['pos']))))

	outReportFile = open(outReportFileName,'w')
	
	for (key, juncH) in juncKH:
		
		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, key[0][0]+':'.join(key[0][1:]), key[1][0]+':'.join(key[1][1:]),\
			juncH['exonLP'][0], juncH['exonLP'][1],\
			juncH['match'] ,-1, len(juncH['pos'])))


optL, argL = getopt.getopt(sys.argv[1:],'i:r:s:',[])

optH = mybasic.parseParam(optL)

if '-s' in optH:
	sampN = optH['-s']
else:
	sampN = optH['-i']

main(optH['-i'],optH['-r'],sampN)
