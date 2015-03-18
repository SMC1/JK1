#!/usr/bin/python

import sys, os, weblogolib
import mybasic

def mutect_weblogo(inDirN, outDirN):
	sampN = os.path.basename(inDirN)
	outFileN = '%s/%s.weblogo_C2T.input' % (outDirN, sampN)
	pdfFileN = '%s/%s.weblogo_C2T.pdf' % (outDirN, sampN)

	mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*mutect' % inDirN).readlines())
	if mutFileNL == []:
		mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*rerun' % inDirN).readlines())
	
	if len(mutFileNL)>1:
		print 'Multiple input files!'
		sys.exit(1)
	
	mutect_weblogo_sub(sampN, mutFileNL[0], outFileN, pdfFileN)

def mutect_weblogo_sub(sampN, inFileN, outFileN, pdfFileN):
	inFile = open(inFileN, 'r')
	inFile.readline() #comment line
	headerL = inFile.readline().rstrip().split('\t')
	idxH = {}
	for i in range(len(headerL)):
		idxH[headerL[i]] = i

	outFile = open(outFileN,'w')
	for line in inFile:
		colL = line.rstrip().split('\t')
		context = colL[idxH['context']]
		ref = colL[idxH['ref_allele']]
		alt = colL[idxH['alt_allele']]
		status = colL[idxH['judgement']]
		if status == 'REJECT':
			continue

		head = context[:3]
		tail = context[-3:]
		context = head + ref + tail
		if ref not in ['C','T']:
			context = mybasic.rc(context)
			ref = mybasic.rc(ref)
			alt = mybasic.rc(alt)

		if ref == 'C' and alt == 'T':## TMZ context only
			outFile.write('%s\n' % context)
	outFile.flush()
	outFile.close()
	
	fin = open(outFileN,'r')
	seqs = weblogolib.read_seq_data(fin)
	data = weblogolib.LogoData.from_seqs(seqs)
	options = weblogolib.LogoOptions()
	options.show_fineprint = False
	options.first_index = -3
	options.logo_title = sampN
	format = weblogolib.LogoFormat(data, options)
	fout = open(pdfFileN, 'w')
	weblogolib.pdf_formatter(data, format, fout)

if __name__ == '__main__':
#	mutect_weblogo('S302','/EQL3/pipeline/somatic_mutect/S302_T_SS.mutect','S302.weblogo.pdf')
#	mutect_weblogo('S171','/EQL3/pipeline/somatic_mutect/S171_T_SS.mutect','S171.weblogo.pdf')
#	mutect_weblogo('S585','/EQL3/pipeline/somatic_mutect/S585_T_SS.mutect','S585.weblogo.pdf')
	for id in ['IRCR_GBM10_038_T_SS','IRCR_GBM12_199_T_SS','IRCR_GBM14_412_T_SS','IRCR_GBM_363_TM_SS','IRCR_GBM_363_TD_SS','IRCR_GBM14_366_T_SS','IRCR_GBM14_476_T03_SS','S171_T_SS','S302_T_SS']:
		print id
		mutect_weblogo('/EQL3/pipeline/somatic_mutation/%s' % id, '/EQL3/pipeline/somatic_mutation/%s' % id)
