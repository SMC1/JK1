#!/usr/bin/python

import sys, os, re, getopt, glob

sys.path.append('~/JK1/NGS/align')
sys.path.append('~/JK1/NGS/mutation')

import bwa_batch, markDuplicates_batch, realign_batch, pileup_batch


def wxs_seq(baseDir, projectName):

	current_files_list = []
	compared_files_list = []	
	current_files_list = glob.glob(baseDir+'/*')
	
	# compose log string
	html_head_string = '<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>'

	# prep html file
	html_path = '/var/www/html/pipeline_logs/' + projectName + '/'
	file_name_split = baseDir.split('/S')
	sample_name = 'S' + file_name_split[1]
	file_name = 'pipeline1_log_' + sample_name + '.html'
	# create .html file
	with open(os.path.join(html_path, file_name), 'wb') as log_file:
		log_file.write(html_head_string)
	log_file.close()	
	
	# change mode and open log_file again
	os.system('chmod 755 %s%s' % (html_path, file_name))
	log_file_name = html_path + file_name
	log_file = open(log_file_name, 'w')

	#----------------------------------------------------------------------------------------------------------------
	# Step1 : execute bwa_batch.py
	# .fq -> .sam -> .bam -> sorted.bam
	try :
		log_file.write('<b> Step1 is starting ... </b><br>')
		bwa_batch.align(baseDir, baseDir, '(.*)\.[12]\.fq', 10, 40000000000, False, 'hg19', False) # WXS
	except:
		log_file.write('<b> Step1 is failed </b><br>')
		sys.exit()

	# write bwa_log string
	# read qlog file and write to .html
	bwa_qlog = baseDir + '/' + sample_name + '.bwa.qlog'
	bwa_qlog_file = open(bwa_qlog, 'r')
	for bwa_qlog_line in bwa_qlog_file:
		log_file.write(bwa_qlog_line)
		log_file.write('<br>')
	bwa_qlog_file.close()
	log_file.write('<br><br>')

	# compose string var - list of files that bwa step has created 
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list
	bwa_str = '<b>step1- bwa successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		bwa_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		bwa_str += bwa_file_item
	bwa_str += '<hr>'
	log_file.write(bwa_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	# Step2 : execute markDuplicates_batch.py
	# sorted.bam -> dedup.bam -> RG.bam
	try:
		markDuplicates_batch.main(baseDir, baseDir, False)
		log_file.write('<b> Step2 is starting ... </b><br>')
	except:
		log_file.write('<b> Step2 is failed </b><br>')
		sys.exit()

	# write mark_dup log string
	# read qlog file and write to .html
	dedup_qlog = baseDir + '/' + sample_name + '.dedup.qlog'
	dedup_qlog_file = open(dedup_qlog, 'r')
	for dedup_qlog_line in dedup_qlog_file:
		log_file.write(dedup_qlog_line)
		log_file.write('<br>')
	dedup_qlog_file.close()
	log_file.write('<br><br>')

	# compose string var - list of files that markDup step has created
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	duplicates_str = '<b>step2- mark duplicating successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		dup_file_item = '-- '  + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		duplicates_str += dup_file_item
	duplicates_str += '<hr>'
	log_file.write(duplicates_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	# Step3 : execute realign_batch.py
	# RG.bam -> realign.bam -> recal.bam
	try:	
		realign_batch.main(baseDir, baseDir, False)	
		log_file.write('<b> Step3 is starting ... </b><br>')
	except:
		log_file.write('<b> Step3 is failed </b><br>')
		sys.exit()

	# write realign_log string
	# read qlog file and write to .html
	realign_qlog = baseDir + '/' + sample_name + '.realign.qlog'
	realign_qlog_file = open(realign_qlog, 'r')
	for realign_qlog_line in realign_qlog_file:
		log_file.write(realign_qlog_line)
		log_file.write('<br>')
	realign_qlog_file.close()
	log_file.write('<br><br>')

	# compose string var - list of files that realign step has created
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir+'/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	realign_str = '<b>step3- realigning successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		realign_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		realign_str += realign_file_item
	realign_str += '<hr>'
	log_file.write(realign_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	# Step4 : mpileup
	try:
		pileup_batch.main(baseDir, baseDir, False)
		log_file.write('<b> Step4 is starting ... </b><br>')
	except:
		log_file.write('<b> Step4 is failed </b><br>')
		sys.exit()

	# write pileup_log string
	# read qlog file and write to .html
	pileup_qlog = baseDir + '/' + sample_name + '.pileup.qlog'
	pileup_qlog_file = open(pileup_qlog, 'r')
	for pileup_qlog_line in pileup_qlog_file:
		log_file.write(pileup_qlog_line)
		log_file.write('<br>')
	pileup_qlog_file.close()
	log_file.write('<br><br>')

	# compose string var - list of files that pileup has created
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir + '/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	pileup_str = '<b>step4- pileup successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		pileup_file_item = '-- '+ str(i) + '.' + str(compared_files_list[i]) + '<br>'
		pileup_str += pileup_file_item
	pileup_str += '<hr>'
	log_file.write(pileup_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	
	log_file.close()

#optL, argL = getopt.getopt(sys.argv[1:], 'i:n:', [])
#optH = mybasic.parseParam(optL)
#baseDir = optH['-i']
#projectName = optH['-n']
#wxs_seq(baseDir,projectName)


#-----------------------
#test method
if __name__ == '__main__':
	wxs_seq('/home/yenakim/YN/linked_fq/S780_T_SS', 'test_cases')
