#!/usr/bin/python

import sys

def main(outDirName):

	nameL = ('ProbeName','ChrName','Start','Stop','437_US91703680_252206016154_S01_CGH_107_Sep09_1_2(437)','559_US91703680_252206011010_S01_CGH_107_Sep09_1_1_559')

	outFile = open('%s/paired_df_CNA_prb_437.txt' % (outDirName),'w')
	outFile.write('%s\t%s\t%s\t%s\t%s\n' % ('sId_p','sId_r','geneN','val_p','val_r'))

	inCNAprobeFile = open('/EQL1/NSL/CGH/NSL_GBM_CGH_109_probe_chr13.txt')
	
	datFile_437 = open('/EQL1/NSL/CGH/S437_prb.dat','w')
	datFile_437.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('ID','chrom','loc.start','loc.end','num.mark','value'))
	datFile_559 = open('/EQL1/NSL/CGH/S559_prb.dat','w')
	datFile_559.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('ID','chrom','loc.start','loc.end','num.mark','value'))

	headerL = inCNAprobeFile.readline()[:-1].split('\t')
	
	idxH = dict([(x, headerL.index(x)) for x in nameL])

	for line in inCNAprobeFile:

		valueL = line[:-1].split('\t')

		prbName = valueL[idxH['ProbeName']]
		chrNum = valueL[idxH['ChrName']]
		chrSta = valueL[idxH['Start']]
		chrEnd = valueL[idxH['Stop']]

		vP = float(valueL[idxH['437_US91703680_252206016154_S01_CGH_107_Sep09_1_2(437)']])
		vR = float( valueL[idxH['559_US91703680_252206011010_S01_CGH_107_Sep09_1_1_559']])

		outFile.write('S437\tS559\t%s\t%.2f\t%.2f\n' % (chrSta,vP,vR))
		datFile_437.write('S437\t%s\t%s\t%s\tNA\t%s\n' % (chrNum,chrSta,chrEnd,vP))
		datFile_559.write('S559\t%s\t%s\t%s\tNA\t%s\n' % (chrNum,chrSta,chrEnd,vR))

	outFile.close()
	datFile_437.close()
	datFile_559.close()

main('/EQL1/PrimRecur/paired')
