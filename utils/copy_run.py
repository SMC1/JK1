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

#	main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL2/SGI_20131226/RNASeq/fastq/link', outputPLDir='/EQL3/pipeline', pType='rsq2expr', projN='SGI20131226_rsq2expr', dryRun=False)
#	main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL2/SGI_20131226/RNASeq/fastq/link', outputPLDir='/EQL3/pipeline', pType='rsq2mut', projN='SGI20131226_rsq2mut', dryRun=False)
#	main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL3/pipeline/SGI20131226_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2eiJunc', projN='SGI20131226_rsq2eiJunc', dryRun=False)
#	main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL3/pipeline/SGI20131226_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2fusion', projN='SGI20131226_rsq2fusion', dryRun=False)
#	main(inputPLDir='/EQL1/pipeline', newFQDir='/EQL3/pipeline/SGI20131226_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2skip', projN='SGI20131226_rsq2skip', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/SGI_20140219/WXS/fastq/link', outputPLDir='/EQL2/pipeline', pType='xsq2mut', projN='SGI20140219_xsq2mut', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/SGI_20131212/WXS/fastq/link', outputPLDir='/EQL2/pipeline', pType='xsq2mut', projN='SGI20131212_xsq2mut', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/SGI_20131212/RNASeq/fastq/link', outputPLDir='/EQL2/pipeline', pType='rsq2mut', projN='SGI20131212_rsq2mut', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/pipeline/SGI20131212_rsq2mut', outputPLDir='/EQL2/pipeline', pType='rsq2eiJunc', projN='SGI20131212_rsq2eiJunc', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/pipeline/SGI20131212_rsq2mut', outputPLDir='/EQL2/pipeline', pType='rsq2fusion', projN='SGI20131212_rsq2fusion', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/pipeline/SGI20131212_rsq2mut', outputPLDir='/EQL2/pipeline', pType='rsq2skip', projN='SGI20131212_rsq2skip', dryRun=False)
#	main(inputPLDir='/EQL2/pipeline', newFQDir='/EQL2/SGI_20140331/WXS/fastq/link', outputPLDir='/EQL3/pipeline', pType='xsq2mut', projN='SGI20140331_xsq2mut', dryRun=False)
#	main(inputPLDir='/EQL6/pipeline', newFQDir='/EQL2/SGI_20140520/RNASeq/fastq/link', outputPLDir='/EQL3/pipeline', pType='rsq2expr', projN='SGI20140520_rsq2expr', dryRun=False)
#	main(inputPLDir='/EQL6/pipeline', newFQDir='/EQL2/SGI_20140520/RNASeq/fastq/link', outputPLDir='/EQL3/pipeline', pType='rsq2mut', projN='SGI20140520_rsq2mut', dryRun=False)
#	main(inputPLDir='/EQL6/pipeline', newFQDir='/EQL3/pipeline/SGI20140520_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2eiJunc', projN='SGI20140520_rsq2eiJunc', dryRun=False)
#	main(inputPLDir='/EQL6/pipeline', newFQDir='/EQL3/pipeline/SGI20140520_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2fusion', projN='SGI20140520_rsq2fusion', dryRun=False)
#	main(inputPLDir='/EQL6/pipeline', newFQDir='/EQL3/pipeline/SGI20140520_rsq2mut', outputPLDir='/EQL3/pipeline', pType='rsq2skip', projN='SGI20140520_rsq2skip', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/CS_20140327/WXS/fastq/link', outputPLDir='/EQL2/pipeline', pType='xsq2mut', projN='CS20140327_xsq2mut', dryRun=False)
#	main(inputPLDir='/EQL3/pipeline', newFQDir='/EQL2/CS_20140526/WXS/fastq/link', outputPLDir='/EQL2/pipeline', pType='xsq2mut', projN='CS20140526_xsq2mut', dryRun=False)

# move to new space
	import re
#	for dir in filter(lambda x: 'rsq2mut' in x and 'SGI' in x, os.listdir('/EQL4/pipeline')):
#		date = re.search('SGI([0-9]{8})_rsq2mut', dir).group(1)
#		FQDir = '/EQL2/SGI_%s/RNASeq/fastq/link' % date
#		if os.path.isdir(FQDir):
#			main(inputPLDir='/EQL4/pipeline', newFQDir=FQDir, outputPLDir='/EQL8/pipeline', pType='rsq2mut', projN=dir, dryRun=False)
#			proj='SGI%s_rsq2expr' % date
#			main(inputPLDir='/EQL4/pipeline', newFQDir=FQDir, outputPLDir='/EQL8/pipeline', pType='rsq2expr', projN=proj, dryRun=False)
#		for t in ['rsq2eiJunc','rsq2fusion','rsq2skip']:
#			FQDir = '/EQL8/pipeline/SGI%s_rsq2mut' % (date)
#			if os.path.isdir('/EQL4/pipeline/SGI%s_%s' % (date, t)):
#				proj='SGI%s_%s' % (date, t)
#				main(inputPLDir='/EQL4/pipeline', newFQDir=FQDir, outputPLDir='/EQL8/pipeline', pType=t, projN=proj, dryRun=False)
	for dir in filter(lambda x: 'rsq2' in x and 'SGI' in x, os.listdir('/EQL2/pipeline')):
		cmd = 'diff -r -x *fq -x *gz -x *bam -x *bai -x *zip /EQL2/pipeline/%s /EQL8/pipeline/%s' % (dir,dir)
		print cmd
		os.system(cmd)
