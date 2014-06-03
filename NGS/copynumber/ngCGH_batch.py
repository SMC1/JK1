#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inputDirN, outputDirN, windowSize=1000, pbs=False, isCS=False):
	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.recal\.bam', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	tumorFileNL = filter(lambda x: re.match('.*_T.{,2}_.*', x), inputFileNL)
	tumorFileNL.sort()

	normalFileNL = list(set(inputFileNL).difference(set(tumorFileNL)))
	normalFileNL.sort()

	for tumorFileN in tumorFileNL:
		if len(normalFileNL) == 1:
			normalFileN = normalFileNL[0]
		else:
			continue

		tumorSampN = re.match('(.*)\.recal\.bam', tumorFileN).group(1)
		normalSampN = re.match('(.*)\.recal\.bam', normalFileN).group(1)
		print tumorSampN, normalSampN

		if isCS:
			dnTumorFileN='%s.recal.DN.bam' % (tumorSampN)
			cmd='java -jar /home/tools/picard-tools-1.73/DownsampleSam.jar I=%s/%s O=%s/%s P=0.15 CREATE_INDEX=True VALIDATION_STRINGENCY=LENIENT' % (inputDirN,tumorFileN, outputDirN,dnTumorFileN)
			cmd='%s; /usr/bin/ngCGH -w %d -o %s/%s.ngCGH %s/%s %s/%s' % (cmd, windowSize, outputDirN,tumorSampN, inputDirN,normalFileN, outputDirN,dnTumorFileN)
			log='%s/%s.cn_ngCGH.log' % (outputDirN, tumorSampN)
			print cmd
		else:
#			cmd = 'samtools index %s/%s; samtools index %s/%s' % (inputDirN,normalFileN, inputDirN,tumorFileN)
#			cmd = '%s; ngCGH -w %d -o %s/%s.ngCGH %s/%s %s/%s' % (cmd, windowSize, outputDirN,tumorSampN, inputDirN,normalFileN, inputDirN,tumorFileN)
			cmd = '/usr/bin/ngCGH -w %d -o %s/%s.ngCGH %s/%s %s/%s' % (windowSize, outputDirN,tumorSampN, inputDirN,normalFileN, inputDirN,tumorFileN)
			log = '%s/%s.cn_ngCGH.log' % (outputDirN, tumorSampN)
			print cmd

		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j os' % (cmd, tumorSampN, log))
		else:
			os.system('(%s) 2> %s' % (cmd, log))

if __name__ == '__main__':
#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:w:',[])
#
#	optH = mybasic.parseParam(optL)
	main('/EQL2/pipeline/CS20140512_xsq2mut/IRCR_GBM14_422_T_CS', '/EQL3/pipeline/CNA', windowSize=1000,pbs=False)

#	main('/EQL3/pipeline/CNA/S641_T_SS', '/EQL3/pipeline/CNA/S641_T_SS', windowSize=1000, pbs=False)
