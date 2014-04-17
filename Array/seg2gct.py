#!/usr/bin/python_epd

import sys, getopt
import mygp, mygenome


optL, argL = getopt.getopt(sys.argv[1:],'',['inSegFile=', 'inRefFlatFile=', 'geneNames=', 'assembly=', 'outGctFile='])
optH = mygp.parseParam(optL)

if '--inSegFile' in optH:
	inSegFileName = optH['--inSegFile']
else:
	inSegFileName = '/Users/jinkuk/Data/TCGA/GBM/Copy_Number_Results/MSKCC__HG-CGH-244A/TCGA_GBM_CN_MSKCC.seg'

if '--inRefFlatFile' in optH:
	inRefFlatFileName = optH['--inRefFlatFile']
else:
	inRefFlatFileName = '/Users/jinkuk/Data/DB/refFlat_hg18.txt'

if '--assembly' in optH:
	assembly = optH['--assembly']
else:
	assembly = 'hg18'

if '--geneNames' in optH:
	geneNameL = optH['--geneNames'].split(';')
else:
	geneNameL = []

if '--outGctFile' in optH:
	outGctFile = open(optH['--outGctFile'], 'w')
else:
	outGctFile = sys.stdout


if geneNameL == []:
	
	geneNameL = list(set([line.split('\t')[0] for line in open(inRefFlatFileName)]))
	geneNameL.sort()

inSegFileMem = [line[:-1].split('\t') for line in open(inSegFileName)]

sIdL = list(set([tokL[0] for tokL in inSegFileMem]))
sIdL.sort()

#outGctFileName = '%s.gct' % mygp.stripPath(inSegFileName)[0]
#outGctFile = open(outGctFileName,'w')

outGctFile.write('#1.2\n')
outGctFile.write('%s\t%s\n' % (len(geneNameL),len(sIdL)))
outGctFile.write('NAME\tDescription\t%s\n' % '\t'.join(sIdL))

for geneName in geneNameL:

	print geneName

	trans = mygenome.transcript(geneName,inRefFlatFileName,assembly)

	h = {}

	for sId in sIdL:
		h[sId] = 0.

	for tokL in inSegFileMem:

		(sId,chrNum,chrSta,chrEnd,numMarker,value) = tokL

		if chrNum != trans.chrNum or value in ('NA','null','NULL'):
			continue

		overlap = trans.cdsOverlap((chrNum,int(chrSta),int(chrEnd)))

		if overlap > 0:
			h[sId] += overlap/float(trans.cdsLen) * float(value)

	outGctFile.write('%s\t' % geneName)

	for sId in sIdL:
		outGctFile.write('\t%s' % h[sId])

	outGctFile.write('\n')

outGctFile.flush()
outGctFile.close()
