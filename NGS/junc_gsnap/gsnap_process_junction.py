#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def gsnap_process_junction(inGsnapFileName,outGsnapFileName,outReportFileName):

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

		transcript1 = re.search('label_[12]:([^,\t]*)', match.segL[0][3])
		
		if transcript1:
			transcript1 = tuple([x.split('.exon')[0] for x in transcript1.group(1).split('|')])
		else:
			transcript1 = ()

		transcript2 = re.search('label_[12]:([^,\t]*)', match.segL[1][3])

		if transcript2:
			transcript2 = tuple([x.split('.exon')[0] for x in transcript2.group(1).split('|')])
		else:
			transcript2 = ()

		s1 = match.segL[0][2]
		s2 = match.segL[1][2]

		bp1 = re.match('[+-]([^:]+):[0-9]+..([0-9]+)',s1)
		bp2 = re.match('[+-]([^:]+):([0-9]+)..[0-9]+',s2)

		if bp1.groups() < bp2.groups():
			key = (bp1.groups(),bp2.groups())
			transcript = (transcript1,transcript2)
		else:
			key = (bp2.groups(),bp1.groups())
			transcript = (transcript2,transcript1)

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['reg'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'splice_type':splice_type, 'seq':[r.seq()], 'reg':[(direction,offset)], 'transcript':transcript}


	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['reg'])),len(set(x[1]['reg']))))

	outGsnapFile = open(outGsnapFileName,'w')
	outReportFile = open(outReportFileName,'w')

	for (key, juncH) in juncKH:

		if key[0][0] == key[1][0]:
			type = 'intra'
		else:
			type = 'inter'

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (type, juncH['splice_type'], key, juncH['transcript'], len(juncH['match']), len(set(juncH['seq'])), len(set(juncH['reg']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')

optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	gsnap_process_junction(optH['-i'],optH['-o'],optH['-r'])
