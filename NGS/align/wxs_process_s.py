#!/usr/bin/python

import sys, os, re, getopt, glob

sys.path.append('/home/heejin/JK1/NGS/align')
sys.path.append('/home/heejin/JK1/NGS/mutation')

import mybasic, mygenome, bwa_batch, markDuplicates_batch, realign_batch, pileup_batch


def wxs_seq(baseDir):
	
	current_files_list = []
	compared_files_list = []	
	
	current_files_list = glob.glob(baseDir+'/*')
	#-------------------------------------------------------------------------------------------------------------
	# Step0 : linking
	#try :
	#	link_fastq.link('/home/yenakim/YN/fastqtest', '/home/yenakim/YN/linked_fq', '.*([0-9]{3}).*')
	#except:
	#	print('step0- linking is failed')

	#get linking_log string
	#current_files_list = glob.glob('/home/yenakim/YN/linked_fq/*')
	#link_string = '<b>step0- linking successfully created files with links below : </b><br>'
	#for i in range(len(current_files_list)):
	#	link_file_item = '-- ' + str(i) + '.' + str(current_files_list[i]) + '<br>'
	#	link_string += link_file_item
	#------------------------------------------------------------------------------------------------------------


	# Step1 : execute bwa_batch.py
	# .fq -> .sam -> .bam -> sorted.bam
	try :
		bwa_batch.align(baseDir, baseDir, '(.*)\.[12]\.fq.gz', 4, 10000000000, False, 'hg19', True) # WXS
	except:
		print('step1 is failed')


	#get bwa_log string
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list
	
	file = tmp_files_list[0]
	file_name_split = file.split(".bwa")
	sample_name = file_name_split[0]

	bwa_string = '<b>step1- bwa successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		bwa_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		bwa_string += bwa_file_item

	# Step2 : execute markDuplicates_batch.py
	# sorted.bam -> dedup.bam -> RG.bam
	try:
		markDuplicates_batch.main(baseDir, baseDir, False)
	except:
		print('step2 is failed')


	#get mark_dup log string
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	duplicates_string = '<b>step2- mark duplicating successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		dup_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		duplicates_string += dup_file_item

	# Step3 : execute realign_batch.py
	# RG.bam -> realign.bam -> recal.bam
	try:	
		realign_batch.main(baseDir, baseDir, False)	
	except:
		print('step3 is failed')

	#get realign_log string
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	realign_string = '<b>step3- realigning successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		realign_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		realign_string += realign_file_item

	# Step4 : mpileup
	try:
		pileup_batch.main(baseDir, baseDir, False)
	except:
		print('step4 is failed')


	#get pileup_log string
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir + '/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	#pileup_files = glob.glob('/home/yenakimi/YN/linked_fq/*.pileup*')
	pileup_string = '<b>step4- pileup successfully created files below : </b><br>'

	for i in range(len(compared_files_list)):
		pileup_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		pileup_string += pileup_file_item

	#compose whole log string
	whole_log_string = '<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>' + bwa_string + duplicates_string + realign_string + pileup_string + '</body></html>'

	#write html file
	html_path = '/var/www/html/'

	file_name = 'pipeline_log_' + sample_name + '.html'
	#file_name = 'pipeline_log.html'
	with open(os.path.join(html_path, file_name), 'wb') as temp_file:
		temp_file.write(whole_log_string)
		temp_file.close()

	#os.system('chmod 777 %s' % file_name)

optL, argL = getopt.getopt(sys.argv[1:], 'i:', [])

optH = mybasic.parseParam(optL)

baseDir = optH['-i']

wxs_seq(baseDir)
