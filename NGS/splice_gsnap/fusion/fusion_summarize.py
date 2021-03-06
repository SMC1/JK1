#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def fusion_summarize(inputDirN,minNPos):

	resultF = os.popen('cat %s/*_splice_transloc_annot1.report_annot.txt | sort -t $"\t" -nrk25' % inputDirN)
	#resultF = os.popen('cat %s/*_splice_transloc_annot1.report_annot.txt | cut -f1,6-9,12-16,19-22,24,28-34' % inputDirN)

	print 'SampleName\tArrangementType\tInter_Intra\tPos1\tPos2\tTransExon1\tTransExon2\tGeneName1\tGeneName2\tCodingFrame\tCNA1\tCNA2\tDesc1\tDesc2\tCensus1\tCensus2\tGO1\tKEGG1\tBIOC1\tGO2\tKEGG2\tBIOC2\t#Reads\t#Seqs\t#Positions'

	for line in resultF:

		(sN,arng,type, bp1,bp2, te1,te2, frm, cna1,cna2, gN1,desc1,census1,go1,kegg1,bioc1, gN2,desc2,census2,go2,kegg2,bioc2, reads,seqs,pos) = \
			line[:-1].split('\t')

		sN = sN.replace('.','_').replace('-','_')
		if int(pos) >= minNPos:

			print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % \
				(sN,arng,type,bp1,bp2,te1,te2, gN1,gN2, frm, cna1,cna2, desc1,desc2, census1,census2,\
				go1,kegg1,bioc1, go2,kegg2,bioc2, reads,seqs,pos)

def fusion_summarize_s(inputFileN, minNPos=1, outFileN=''):
	resultF = os.popen('cat %s | sort -t $"\t" -nrk25' % inputFileN)
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')

	outFile.write('SampleName\tArrangementType\tInter_Intra\tPos1\tPos2\tTransExon1\tTransExon2\tGeneName1\tGeneName2\tCodingFrame\tCNA1\tCNA2\tDesc1\tDesc2\tCensus1\tCensus2\tGO1\tKEGG1\tBIOC1\tGO2\tKEGG2\tBIOC2\t#Reads\t#Seqs\t#Positions\n')
	for line in resultF:
		(sN,arng,type, bp1,bp2, te1,te2, frm, cna1,cna2, gN1,desc1,census1,go1,kegg1,bioc1, gN2,desc2,census2,go2,kegg2,bioc2, reads,seqs,pos) = line[:-1].split('\t')

		sN = sN.replace('.','_').replace('-','_')
		if int(pos) >= minNPos:
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
				(sN,arng,type,bp1,bp2,te1,te2, gN1,gN2, frm, cna1,cna2, desc1,desc2, census1,census2,\
				go1,kegg1,bioc1, go2,kegg2,bioc2, reads,seqs,pos))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

	optH = mybasic.parseParam(optL)

	#inputDirN = optH['-i']
	#fusion_summarize(inputDirN)

	#fusion_summarize('/EQL1/NSL/RNASeq/results/fusion',1)
	#fusion_summarize('/EQL4/SGI_20131031/RNASeq/pipeline/SGI20131031_rsq2fusion/*', 1)
	#fusion_summarize('/EQL1/pipeline/SGI20131119_rsq2fusion/*',1)
	fusion_summarize('/EQL1/pipeline/SGI20131212_rsq2fusion/*',1)
