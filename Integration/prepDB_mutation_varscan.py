#!/usr/bin/python

# for varscan output

import sys, getopt, re,	os 
import mybasic

def main(inDirName,sampNamePat=('(.*)',''),geneList=[]):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('(.*)_snp_cosmic\.dat', x),inputFileNL)

	sIdL = [re.match(sampNamePat[0], x).group(1) for x in inputFileNL]

	for inFileN in inputFileNL:

		sId = re.match(sampNamePat[0], inFileN).group(1)

		if 'Br' in inFileN:
			sId = sId+'_X'
			
		if sIdL.count(sId) > 1:
			if 'Kinome' in inFileN or '_B_' in inFileN:
				continue
		
		inFile = open('%s/%s' % (inDirName,inFileN))

		for line in inFile:

			valueL = line[:-1].split('\t')

			sampN = valueL[0]


			chrom = valueL[1]
			chrSta = valueL[2]
			chrEnd = valueL[3]

			ref = valueL[4]
			alt = valueL[5]

			nReads_ref = valueL[6]
			nReads_alt = valueL[7]

			strand = valueL[8]

			geneN = valueL[9]

			ch_dna = valueL[10]
			ch_aa = valueL[11]
			ch_type = valueL[12]

			if 'silent' in ch_type:
				continue

			cosmic = valueL[11]

			mutsig = ''


			sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
				(sId, chrom,chrSta,chrEnd, ref,alt, nReads_ref, nReads_alt, strand, \
				geneN, ch_dna, ch_aa, ch_type, cosmic, mutsig))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/exome_bam/mutation',('.*([0-9]{3}).*',''),[])
