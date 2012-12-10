#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def fusion_proc_sort(inGsnapFileName,outGsnapFileName,outReportFileName,sampN):

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	juncHH = {}

	for r in result:

		match = r.matchL()[0]

		if not '(transloc)' in r.pairRel:
			raise Exception

		if len(match.segL) != 2:
			raise Exception

		splice_type = re.search('splice_type:([^,\t]*)', match.segL[0][3]).group(1)
		direction = re.search('dir:([^,\t]*)', match.segL[0][3]).group(1)
		offset = int(re.search('\.\.([0-9]*)', match.segL[0][1]).group(1))

		transcriptL = []

		for i in range(2):

			rm = re.search('label_[12]:([^,\t]*)', match.segL[i][3])

			if rm:
				transcriptL.append(rm.group(1).replace('|',','))
			else:
				transcriptL.append('')

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
			transcriptL = transcriptL[::-1]
		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['pos'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'splice_type':splice_type, 'seq':[r.seq()], 'pos':[(direction,offset)], 'transcript':transcriptL}

	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['pos'])),len(set(x[1]['pos']))))

	outGsnapFile = open(outGsnapFileName,'w')
	outReportFile = open(outReportFileName,'w')

	for (key, juncH) in juncKH:

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(juncH['splice_type'], sampN, key[0][0]+':'.join(key[0][1:]), key[1][0]+':'.join(key[1][1:]), \
			juncH['transcript'][0], juncH['transcript'][1],  \
			len(juncH['match']), len(set(juncH['seq'])), len(set(juncH['pos']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')

# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:s:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	if '-s' in optH:
		fusion_proc_sort(optH['-i'],optH['-o'],optH['-r'],optH['-s'])
	else:
		fusion_proc_sort(optH['-i'],optH['-o'],optH['-r'],optH['-i'])
