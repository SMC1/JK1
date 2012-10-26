#!/usr/bin/python

import sys, getopt
import mygp, CanGen


optL, argL = getopt.getopt(sys.argv[1:],'',['inGctFile=', 'geneName=', 'dataName='])
optH = mygp.parseParam(optL)

if '--inGctFile' in optH:
	inGctFileName = optH['--inGctFile']
else:
	inGctFileName = 'TCGA_GBM_CNA_SNP6.gct'

if '--geneNames' in optH:
	geneNames = optH['--geneNames']
else:
	geneNames = 'EGFR,CDK4'

if '--dataName' in optH:
	dataName = optH['--dataName']
else:
	dataName = 'TCGA_GBM_CNA_SNP6'


plat = 'x'

geneNameL = geneNames.split(',')

outFile = open('%s_%sgenes.dst' % (dataName,len(geneNameL)),'w')

for geneName in geneNameL:

	geneName = geneName.upper()

	indH = CanGen.loadGct({}, [geneName], inGctFileName, plat)

	valueL = [(x.sId,x.expr[plat][geneName]) for x in indH.values()]
	valueL.sort(lambda x,y: cmp(x[1],y[1]))

	outFile.write('%s\n' % dataName)
	outFile.write('%s\n' % geneName)
	outFile.write('%s\n' % '\t'.join(map(str,[x[1] for x in valueL])))
	outFile.write('%s\n' % '\t'.join(map(str,[x[0] for x in valueL])))

outFile.close()
