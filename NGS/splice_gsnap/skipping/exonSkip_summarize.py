#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def exonSkip_summarize(inputDirN,minPos=2):

	resultF = os.popen('cat %s/*/*_splice_exonSkip_report_annot.txt | sort -t $"\t" -nrk16' % inputDirN)
#	resultF = os.popen('cat %s/*_splice_exonSkip_report_annot.txt | sort -t $"\t" -nrk16' % inputDirN)
	#resultF = os.popen('cat %s/*_splice_transloc_annot1.report_annot.txt | cut -f1,6-9,12-16,19-22,24,28-34' % inputDirN)

	print 'SampleName\tPos1\tPos2\tTransExon1\tTransExon2\tGeneName\tCodingFrame\tCNA\tDesc\tCensus\tGO\tKEGG\tBIOC\t#Reads\t#Seqs\t#Positions'

	for line in resultF:

		(sN, bp1,bp2, te1,te2, frm,gN,cna, desc,census, go,kegg,bioc, reads,seqs,pos) = \
			line[:-1].split('\t')

		sN = sN.replace('.','_').replace('-','_')
		if int(pos) >= int(minPos):
			print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % \
				(sN,bp1,bp2,te1,te2, gN,frm,cna,desc,census, go,kegg,bioc, reads,seqs,pos)

def exonSkip_summarize_s(inFileN, minPos=2, outFileN=''):
	resultF = os.popen('cat %s | sort -t $"\t" -nrk16' % inFileN)

	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')

	outFile.write('SampleName\tPos1\tPos2\tTransExon1\tTransExon2\tGeneName\tCodingFrame\tCNA\tDesc\tCensus\tGO\tKEGG\tBIOC\t#Reads\t#Seqs\t#Positions\n')
	for line in resultF:
		(sN, bp1,bp2, te1,te2, frm,gN,cna, desc,census, go,kegg,bioc, reads,seqs,pos) = line[:-1].split('\t')
		sN = sN.replace('.','_').replace('-','_')
		if int(pos) >= int(minPos):
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
				(sN,bp1,bp2,te1,te2, gN,frm,cna,desc,census, go,kegg,bioc, reads,seqs,pos))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:n:',[])

	optH = mybasic.parseParam(optL)

	#inputDirN = optH['-i']
	#
	#if '-n' in optH:
	#	exonSkip_summarize(inputDirN,optH['-n'])
	#else:
	#	exonSkip_summarize(inputDirN)

	#exonSkip_summarize('/EQL2/TCGA/LUAD/RNASeq/skipping/exonskip',1)
	#exonSkip_summarize('/EQL1/NSL/RNASeq/results/exonSkip',1)
	#exonSkip_summarize('/EQL1/pipeline/SGI20131031_rsq2skip',1)
	#exonSkip_summarize('/EQL1/pipeline/SGI20131119_rsq2skip',1)
	exonSkip_summarize('/EQL1/pipeline/SGI20131212_rsq2skip',1)
