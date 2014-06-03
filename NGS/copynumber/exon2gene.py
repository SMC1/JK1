#!/usr/bin/python

import sys, getopt, math, re
import mybasic, mygenome

def main(inSegFileName, inRefFlatFileName, outFileName, geneNameL, assembly='hg19'):

	(sid, postfix) = re.match('(.*)_([TXC].{,2})_.*.copynumber', inSegFileName.split('/')[-1]).groups()
	if postfix != 'T':
		sampN = sid + '_' + postfix
	else:
		sampN = sid
	
	if geneNameL == []:
		geneNameL = list(set([line.split('\t')[0] for line in open(inRefFlatFileName)]))
		geneNameL.sort()

	inSegFileMem = [line[:-1].split('\t') for line in open(inSegFileName) if line[:-1].split('\t')[0] != 'ID']

	sIdL = list(set([tokL[0] for tokL in inSegFileMem]))
	sIdL.sort()

	outFile = open(outFileName, 'w')
	
	for geneName in geneNameL:
		
		print geneName

		try:
			trans = mygenome.transcript(geneName,inRefFlatFileName,assembly)
		except:
			continue

		h = {}

		for sId in sIdL:
			h[sId] = 0.

		for tokL in inSegFileMem:

			(sId,chrNum,chrSta,chrEnd,numMarker,value) = tokL
			if 'chr' in chrNum:
				chrNum = re.match('chr(.*)', chrNum).group(1)

			if chrNum != trans.chrNum or value in ('NA','null','NULL'):
				continue

			overlap = trans.cdsOverlap((chrNum,int(chrSta),int(chrEnd)))

			if overlap > 0:
				h[sId] += overlap/float(trans.cdsLen) * float(value)

		outFile.write('%s\t%s' % (sampN, geneName))
		
		for sId in sIdL:
			outFile.write('\t%s' % h[sId])

		outFile.write('\n')

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:r:o:g:a:',[])

	optH = mybasic.parseParam(optL)

#	if '-i' in optH and '-o' in optH:
#
#		if '-g' in optH:
#			geneNameL = geneNames.split(',')
#		else:
#			geneNameL = [] 

	geneNameL = ['STK11', 'AKT1', 'AKT2', 'AKT3', 'MLH1', 'ROS1', 'PIK3CA', 'NTRK1', 'CDH1', 'FGFR1', 'ERBB2', 'ERBB3', 'IGF1R', 'CDKN2A', 'PIK3R1', 'ERBB4', 'IDH2', 'IDH1', 'MDM2', 'FGFR2', 'FGFR3', 'KRAS', 'SYK', 'ARID1B', 'PTPN11', 'KIT', 'PTEN', 'APC', 'ITK', 'ARID1A', 'HRAS', 'JAK2', 'JAK3', 'NF1', 'JAK1', 'EPHB4', 'ARID2', 'TP53', 'GNAQ', 'GNAS', 'DDR2', 'MPL', 'TOP1', 'PDGFRB', 'PDGFRA', 'SMAD4', 'ATM', 'RET', 'SMO', 'ABL1', 'FLT3', 'CSF1R', 'KDR', 'FBXW7', 'SRC', 'MTOR', 'ATRX', 'ALK', 'MET', 'EZH2', 'CDK4', 'CDK6', 'BRCA1', 'EGFR', 'CTNNB1', 'VHL', 'BRCA2', 'NRAS', 'RB1', 'HNF1A', 'AURKA', 'AURKB', 'TERT', 'SMARCB1', 'NPM1', 'NOTCH1', 'BRAF', 'GNA11', 'PTCH2', 'PTCH1', 'BCL2']
	
	main(optH['-i'],optH['-r'],optH['-o'],geneNameL,optH['-a'])
