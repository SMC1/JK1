#!/usr/bin/python

import sys, getopt
import mygp, CanGen


optL, argL = getopt.getopt(sys.argv[1:],'',['inGctFile=', 'geneName=', 'dataName='])
optH = mygp.parseParam(optL)

if '--inGctFile' in optH:
	inGctFileName = optH['--inGctFile']
else:
	inGctFileName = '/Users/jinkuk/Data/TCGA/GBM/Expression-miRNA/TCGA_GBM_miRNA.gct'

if '--geneName' in optH:
	geneName = optH['--geneName']
else:
	geneName = 'hsa-miR-9'

if '--dataName' in optH:
	dataName = optH['--dataName']
else:
	dataName = 'TCGA_GBM_miRNA'


plat = 'x'

geneName = geneName.upper()

indH = CanGen.loadGct({}, [geneName], inGctFileName, plat)

valueL = [(x.sId,x.expr[plat][geneName]) for x in indH.values()]
valueL.sort(lambda x,y: cmp(x[1],y[1]))

outFile = open('%s_%s.dst' % (dataName,geneName),'w')

outFile.write('%s\n' % dataName)
outFile.write('%s\n' % geneName)
outFile.write('%s\n' % '\t'.join(map(str,[x[1] for x in valueL])))
outFile.write('%s\n' % '\t'.join(map(str,[x[0] for x in valueL])))

outFile.close()
