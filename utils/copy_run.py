#!/usr/bin/python

import sys, os, getopt
import mybasic
from glob import glob

surfixH = {'xsq2mut': '.Xsq.qlog', 'rsq2mut': '.Rsq_mut.qlog', 'rsq2expr': '.Rsq_expr.qlog', 'rsq2eiJunc': '.Rsq_eiJunc.qlog', 'rsq2fusion': '.Rsq_fusion.qlog', 'rsq2skip': '.Rsq_skip.qlog'}

def main(inputPLDir, newFQDir, pType, projN, server='smc1', genome='hg19', outputPLDir='/pipeline', dryRun=True):
	sampNL = os.popen('ls %s/%s | grep -v html | grep -v qlog' % (inputPLDir, projN)).readlines()

	if not os.path.isdir('%s/%s' % (outputPLDir, projN)):
		cmd = 'mkdir %s/%s' % (outputPLDir, projN)
		print cmd
		if not dryRun:
			os.system(cmd)

	for sampN in map(lambda x: x.rstrip(), sampNL):
		# specific exclusion list
#		if sampN not in map(lambda x: '%s_RSq' % x, ['S1B','S2B','S3A','S3B','S9B','S12B','S13B','S722','S796','S140','S121','S208']):
#		if sampN not in map(lambda x: '%s_RSq' % x, ['S11A','S11B','S12A','S13A']):
#			continue

		if os.path.isdir('%s/%s/%s' % (inputPLDir, projN, sampN)):
			print sampN
			if os.path.isfile('%s/%s/%s.html' % (inputPLDir, projN, sampN)):
				cmd = 'cp %s %s' % (inputPLDir+'/'+projN+'/'+sampN+'.html', outputPLDir+'/'+projN)
				print cmd
				if not dryRun:
					os.system(cmd)
			cmd = 'cp -r %s %s' % (inputPLDir+'/'+projN+'/'+sampN, outputPLDir+'/'+projN)
			print cmd
			if not dryRun:
				os.system(cmd)

			if pType in ['xsq2mut', 'rsq2expr', 'rsq2mut']:
				for i in [1, 2]:
					cmd = 'unlink %s/*.%s.fq.gz' % (outputPLDir+'/'+projN+'/'+sampN, i)
					print cmd
					if not dryRun:
						os.system(cmd)
					new_input = '%s/%s.%s.fq.gz' % (newFQDir, sampN, i)
					new_link = '%s/%s.%s.fq.gz' % (outputPLDir+'/'+projN+'/'+sampN, sampN, i)
					cmd = 'ln -s %s %s' % (new_input, new_link)
					print cmd
					if not dryRun:
						os.system(cmd)
			else:
				cmd = 'unlink %s/%s_splice.gsnap.gz' % (outputPLDir+'/'+projN+'/'+sampN, sampN)
				print cmd
				if not dryRun:
					os.system(cmd)
				new_input = '%s/%s_splice.gsnap.gz' % (newFQDir+'/'+sampN, sampN)
				new_link = '%s/%s_splice.gsnap.gz' % (outputPLDir+'/'+projN+'/'+sampN, sampN)
				cmd = 'ln -s %s %s' % (new_input, new_link)
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
#	main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline',newFQDir='/EQL2/SGI_20131031/RNASeq/fastq/link',pType='rsq2mut',projN='SGI20131031_rsq2mut', dryRun=False)
#	main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline',newFQDir='/EQL4/SGI_20131031/RNASeq/pipeline/SGI20131031_rsq2mut', pType='rsq2fusion', projN='SGI20131031_rsq2fusion', outputPLDir='/EQL4/SGI_20131031/RNASeq',dryRun=True)
	#main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL2/SGI_20131119/WXS/fastq/link', pType='xsq2mut', projN='SGI20131119_xsq2mut', outputPLDir='/EQL3/pipeline', dryRun=False)
	#main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline',newFQDir='/EQL2/SGI_20131031/RNASeq/fastq/link',pType='rsq2mut',projN='SGI20131031_rsq2mut',dryRun=False)
	#main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline', newFQDir='/EQL1/pipeline/SGI20131031_rsq2mut',pType='rsq2skip',projN='SGI20131031_rsq2skip',dryRun=False)
	main(inputPLDir='/EQL4/SGI_20131031/RNASeq/pipeline', newFQDir='/EQL2/SGI_20131119/WXS/fastq/link', outputPLDir='/EQL3/pipeline', pType='xsq2mut', projN='SGI20131119_xsq2mut', dryRun=False)
