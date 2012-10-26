#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2fastq_batch1(inDirName,fileNamePattern,outDirName):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
	
	print 'Samples: %s (%s)' % (nameL, len(nameL))

	for name in nameL:

		#if name[1] in ['05918561-a713-464b-9b5c-4f7c9258a827','091cb252-dd08-4e9c-939c-749f595713f6','0c3f0857-32d7-4ef6-b303-6e452ee04516','14404fa2-adc4-4ecd-b4ee-5f4a75b54ff2','229ebbe9-4dc8-434f-998c-fc0660cd2b00','25be50e7-7705-492d-a44a-0e40180d10c8','27706c21-96cb-48e9-88ec-1c52769bfe45','27e70f84-80c5-4f6c-9d22-83c5a6e66eb5','2af2adfe-bd7b-4eb1-9971-182b11075159','3264f809-4bbf-48e6-bbfd-77eaca9e602e','3610639e-d947-446f-8483-86be65c80ed3','416041ff-f179-4c72-a281-f39d32c595c1','44d93b9f-95d6-4382-9590-f6e7bdda65c5','59783c67-6446-44c1-b9b3-505470f54c82','5b262ec0-72f2-4c54-820e-a39afad67212','66626142-7c5c-4ed0-8ef0-f4133423f275','7157ccb4-b4f6-41ba-9f9c-da862b749a57','7455cc98-aceb-4adc-932b-4fddd979c522','7aa46530-2311-41ed-a452-9ca06f38c0c1','8e7ab480-e75d-49a4-98a6-fcdd2ccefaa7','9a92e20a-2a43-4917-981d-c93179770050','9d64aa0c-84a6-4e48-b28b-12aaf04813b6','c55bb0b8-3417-4142-97f8-c43f1ec56496','cb9d4717-15a8-4499-ae3b-e047e5c2926a','e3639f71-cfe7-46c7-8390-73f8043ac6b0','ec38c31b-def8-41cc-8656-57ce98f3faa7','ed74a7e1-90de-4943-9ca2-e7f94a5540e4','fb0cd718-5300-4447-9740-a63308f65d92','TCGA-04-1331-01A-01R-1569-13','TCGA-04-1337-01A-01R-1564-13','TCGA-09-0369-01A-01R-1564-13','TCGA-13-1488-01A-01R-1565-13','TCGA-24-1550-01A-01R-1566-13','TCGA-24-1928-01A-01R-1567-13','TCGA-25-1316-01A-01R-1565-13','TCGA-25-1877-01A-01R-1567-13','TCGA-29-1697-01A-01R-1567-13','TCGA-29-1774-01A-01R-1567-13','TCGA-31-1959-01A-01R-1568-13','TCGA-59-2350-01A-01R-1569-13','TCGA-61-1738-01A-01R-1567-13','TCGA-61-2102-01A-01R-1568-13'] or name[1][:4] != 'TCGA':
		#if name[1] not in  ['0e8881cf-4745-4fb5-9842-dface6532da3','2b56219d-b0d0-4107-acdf-b2ad9c18f090','34149234-2d6a-46ac-b7e0-52787cf2c49a','9713963c-c7c7-47a0-ba01-6710bd4e9fea','bbe4d7f0-1ed9-4d58-9b59-c71d144f73ab','edd5fa64-d6c2-453f-bc77-ca7e5b00e350']:

		print name

		os.system('java -jar /home/tools/picard-tools-1.73/SamToFastq.jar INPUT=%s/%s FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true' % \
			(inDirName,name[0], outDirName,name[1], outDirName,name[1]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH and '-p' in optH:
#
#	bam2fastq_batch1(optH['-i'], optH['-p'], optH['-o'])
#
#else:

pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam' # GBM
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'
pattern3 = '(TCGA.{24})\.bam' # pre-sorted (BRCA, KIRC, UCEC)
pattern4 = '(.*)_rnaseq.bam' # OV
pattern5 = '(.*).bam'

bam2fastq_batch1('/EQL1/TCGA/NTRK1-outlier/alignment/sortedByName',pattern3,'/EQL1/TCGA/NTRK1-outlier/fastq')
