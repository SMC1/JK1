#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def exonSkip_proc_sort(inGsnapFileName,outGsnapFileName,outReportFileName,sampN):

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
				break

			exonLP.append(rm.group(1))

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
			key = (bp1.groups()[1:],bp2.groups()[1:])

		elif direction=='antisense':
			key = (bp2.groups()[1:],bp1.groups()[1:])
			exonLP = exonLP[::-1]

		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['reg'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'seq':[r.seq()], 'reg':[(direction,offset)], 'exonLP':exonLP}

	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['reg'])),len(set(x[1]['reg']))))

	outGsnapFile = open(outGsnapFileName,'w')
	outReportFile = open(outReportFileName,'w')

	
	for (key, juncH) in juncKH:
		
		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN,':'.join(key[0]), ':'.join(key[1]),\
			juncH['exonLP'][0], juncH['exonLP'][1],\
			len(juncH['match']) ,len(set(juncH['seq'])), len(set(juncH['reg']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')

# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:s:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	if '-s' in optH:
		exonSkip_proc_sort(optH['-i'],optH['-o'],optH['-r'],optH['-s'])
	else:
		exonSkip_proc_sort(optH['-i'],optH['-o'],optH['-r'],optH['-i'])
