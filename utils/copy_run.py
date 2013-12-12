#!/usr/bin/python

import sys, os, getopt
import mybasic
from glob import glob

surfixH = {'rsq2mut': '.Rsq_mut.qlog'}

def main(inputPLDir, newFQDir, pType, projN, server='smc1', genome='hg19', outputPLDir='/pipeline', dryRun=True):
	sampNL = os.popen('ls %s/%s | grep -v html | grep -v qlog' % (inputPLDir, projN)).readlines()

	if not os.path.isdir('%s/%s' % (outputPLDir, projN)):
		os.system('mkdir %s/%s' % (outputPLDir, projN))

	for sampN in map(lambda x: x.rstrip(), sampNL):
		# specific exclusion list
#		if sampN not in map(lambda x: '%s_RSq' % x, ['S1B','S2B','S3A','S3B','S9B','S12B','S13B','S722','S796','S140','S121','S208']):
		if sampN not in map(lambda x: '%s_RSq' % x, ['S11A','S11B','S12A','S13A']):
			continue

		if os.path.isdir('%s/%s/%s' % (inputPLDir, projN, sampN)):
			print sampN
			cmd = 'cp -r %s %s' % (inputPLDir+'/'+projN+'/'+sampN, outputPLDir+'/'+projN)
			print cmd
			if not dryRun:
				os.system(cmd)
			for i in [1, 2]:
				cmd = 'unlink %s/*.%s.fq.gz' % (outputPLDir+'/'+projN+'/'+sampN, i)
				print cmd
				if not dryRun:
					os.system(cmd)
			oLogN = outputPLDir+'/'+projN+'/'+sampN+'/'+sampN+surfixH[pType]
			cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_%s.py -i %s/%s.\*.fq.gz -n %s -p %s -c False -s %s -g %s 2> %s' % (pType, newFQDir,sampN, sampN, projN, server, genome, oLogN)
			print cmd
			if not dryRun:
				os.system(cmd)

if __name__ == '__main__':

#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:f:t:s:g:p:',[])
#	optH = mybasic.parseParam(optL)
#
#	inputPipelineN = optH['-i']
#	outputPipelineN = optH['-o']
#	newFastqDirN = optH['-f']
#	pipelineType = optH['-t']
#	server = optH['-s']
#	genome = optH['-g']
#	projectN = optH['-p']

	#main(inputPipelineN, newFastqDirN, pipelineType, projectN, server, genome, outputPipelineN)
	main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline',newFQDir='/EQL2/SGI_20131031/RNASeq/fastq/link',pType='rsq2mut',projN='SGI20131031_rsq2mut', dryRun=False)
