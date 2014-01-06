#!/usr/bin/python

# for mutscan output

import sys, getopt, re,	os 
import mybasic

def main(sampNamePat=('(.*)',''),geneList=[]):

	inFile = sys.stdin

	for line in inFile:

		valueL = line[:-1].split('\t')

		sampN = valueL[0]

		if sampN in ['S437_T_KN','S559_T_KN','S775_T_KN','S025_T_KN','S047_T_KN','S464_T_KN','S532_T_KN','S780_T_KN']:
			continue

		sId = re.match(sampNamePat[0], sampN).group(1)	

		if '_X_' in sampN and sId[-2:] != '_X':
			sId = sId + '_X'

		if '_B_' in sampN:
			continue

		chrom = valueL[1]
		chrSta = valueL[2]
		chrEnd = valueL[3]

		ref = valueL[4]
		alt = valueL[5]

		nReads_ref = valueL[6]
		nReads_alt = valueL[7]

		if int(nReads_alt) < 2:
			continue

		strand = valueL[8]

		geneN = valueL[9]

		ch_dna = valueL[10]
		ch_aa = valueL[11]
		ch_type = valueL[12]

#		if ch_type == 'Substitution - coding silent' or ch_type == 'synonymous_variant':
#			continue

		cosmic = valueL[11]

		mutsig = ''


		sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sId, chrom,chrSta,chrEnd, ref,alt, nReads_ref, nReads_alt, strand, \
			geneN, ch_dna, ch_aa, ch_type, cosmic, mutsig))
#	inputFileNL = os.listdir(inDirName)
#	inputFileNL = filter(lambda x: re.match('(.*)_cosmic\.dat', x),inputFileNL)
#
#	sIdL = [re.match(sampNamePat[0], x).group(1) for x in inputFileNL]
#
#	for inFileN in inputFileNL:
#
#		sId = re.match(sampNamePat[0], inFileN).group(1)
#		
#		if '_X_' in inFileN:
#			sId = sId+'_X'
#						
#		if sIdL.count(sId) > 1:
#			if '_KN' in inFileN or '_B_' in inFileN:
#				continue
#		
#		inFile = open('%s/%s' % (inDirName,inFileN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

#main(('.*([0-9]{3}).*',''),[])
main(('.{1}(.*)_[BNTX]_[NSKT]{2}',''),[])
