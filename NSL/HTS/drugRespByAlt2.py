#!/usr/bin/python

import sys, os, re, getopt
import mymysql, mybasic

WTSidH = {'592T': 'S592', '626T': 'S626', '723T': '', '775T': 'S775', 'GBM13_235T': '', 'GBM13_352T1': 'IRCR_GBM_352_TL', 'GBM13_352T2': 'IRCR_GBM_352_TR', 'GBM14_458T_M2': 'IRCR_GBM14_458', 'GBM14_485T1_M2': 'IRCR_GBM14_485', 'GBM14_487T_M3': 'IRCR_GBM14_487', 'GBM14_497T_M3': '', 'GBM14_499T1_M3': '', 'GBM14_500T_M8': 'IRCR_GBM14_500', 'GBM14_503T_M3': 'IRCR_GBM14_503', 'GBM14_504T3_M3': 'IRCR_GBM14_504_T03', 'GBM14_508T_M8': 'IRCR_GBM14_508', 'GBM14_524T_M3': 'IRCR_GBM14_524', 'GBM14_526T': 'IRCR_GBM14_526', 'GBM14_527T2': 'IRCR_GBM14_527_T02', 'GBM14_529T': 'IRCR_GBM14_529', 'GBM14_534T': 'IRCR_GBM14_534', 'GBM14_541T': 'IRCR_GBM14_541', 'GBM14_542T': 'IRCR_GBM14_542_T01', 'GBM14_543T': '', 'GBM14_544T': '', 'GBM14_549T1_M8': 'IRCR_GBM14_549_T01', 'GBM14_554T_M8': 'IRCR_GBM14_554_TA', 'GBM14_559T1': 'IRCR_GBM14_559_T01', 'GBM14_559T2': 'IRCR_GBM14_559_T02', 'GBM14_565T': 'IRCR_GBM14_565', 'GBM14_569T': '', 'GBM14_570T1': '', 'GBM14_570T2_M8': 'IRCR_GBM14_570_T02', 'GBM14_571T': 'IRCR_GBM14_571', 'GBM14_574T': 'IRCR_GBM14_574', 'GBM14_576T': 'IRCR_GBM14_576', 'GBM14_586T_M8': 'IRCR_GBM14_586', 'GBM14_588T_M8': 'IRCR_GBM14_588', 'GBM14_591T1': 'IRCR_GBM14_591_T01', 'GBM14_593T': 'IRCR_GBM14_593', 'GBM14_594T2_M8': '', 'GBM14_605T_M8': 'IRCR_GBM14_605', 'GBM14_606T': 'IRCR_GBM14_606', 'GBM14_608T': 'IRCR_GBM14_608', 'GBM14_617T': 'IRCR_GBM14_617', 'GBM14_619T': 'IRCR_GBM14_619_T01', 'GBM14_629T': 'IRCR_GBM14_629', 'GBM14_664T1': 'IRCR_GBM14_664_T01', 'GBM14_664T2_M9': 'IRCR_GBM14_664_T02', 'GBM14_665T1': 'IRCR_GBM14_665_T01', 'GBM14_669T': '', 'GBM15_677T': 'IRCR_GBM15_677', 'GBM15_680T': 'IRCR_GBM15_680', 'GBM15_682T': 'IRCR_GBM15_682', 'GBM15_689T': '', 'GBM15_693T1': 'IRCR_GBM15_693_T01', 'GBM15_693T2': 'IRCR_GBM15_693_T02', 'GBM15_693T4': 'IRCR_GBM15_693_T04', 'GBM15_694T2': 'IRCR_GBM15_694_T02', 'GBM15_694T3': 'IRCR_GBM15_694_T03', 'GBM15_694T5': 'IRCR_GBM15_694_T05', 'GBM15_696T': 'IRCR_GBM15_696', 'GBM15_698T': 'IRCR_GBM15_698', 'GBM15_699T': 'IRCR_GBM15_699', 'GBM15_700T': 'IRCR_GBM15_700', 'GBM15_705T': 'IRCR_GBM15_705', 'GBM15_708T': 'IRCR_GBM15_708_TA', 'GBM15_709T1_M8': 'IRCR_GBM15_709_T01', 'GBM15_714T_M9': 'IRCR_GBM15_714', 'GBM15_717T': '', 'GBM15_718T1': 'IRCR_GBM15_718_T01', 'GBM15_718T2': 'IRCR_GBM15_718_T02', 'GBM15_729T': '', 'GBM15_732T_M8': '', 'GBM15_734T2_M8': '', 'GBM15_756T_M8': '', 'GBM15_757T2_M8': '', 'GBM15_758T_M8': ''}

WESidH = {'592T': '', '626T': 'S626', '723T': 'S723', '775T': '', 'GBM13_235T': '', 'GBM13_352T1': 'IRCR_GBM_352_TL', 'GBM13_352T2': 'IRCR_GBM_352_TR', 'GBM14_458T_M2': 'IRCR_GBM14_458', 'GBM14_485T1_M2': 'IRCR_GBM14_485', 'GBM14_487T_M3': 'IRCR_GBM14_487', 'GBM14_497T_M3': '', 'GBM14_499T1_M3': '', 'GBM14_500T_M8': 'IRCR_GBM14_500', 'GBM14_503T_M3': 'IRCR_GBM14_503', 'GBM14_504T3_M3': 'IRCR_GBM14_504_T03', 'GBM14_508T_M8': 'IRCR_GBM14_508', 'GBM14_524T_M3': 'IRCR_GBM14_524', 'GBM14_526T': 'IRCR_GBM14_526', 'GBM14_527T2': 'IRCR_GBM14_527_T02', 'GBM14_529T': 'IRCR_GBM14_529', 'GBM14_534T': 'IRCR_GBM14_534', 'GBM14_541T': 'IRCR_GBM14_541', 'GBM14_542T': 'IRCR_GBM14_542_T01', 'GBM14_543T': '', 'GBM14_544T': '', 'GBM14_549T1_M8': 'IRCR_GBM14_549_T01', 'GBM14_554T_M8': '', 'GBM14_559T1': 'IRCR_GBM14_559_T01', 'GBM14_559T2': 'IRCR_GBM14_559_T02', 'GBM14_565T': 'IRCR_GBM14_565', 'GBM14_569T': '', 'GBM14_570T1': 'IRCR_GBM14_570_T01', 'GBM14_570T2_M8': 'IRCR_GBM14_570_T02', 'GBM14_571T': '', 'GBM14_574T': 'IRCR_GBM14_574', 'GBM14_576T': 'IRCR_GBM14_576', 'GBM14_586T_M8': 'IRCR_GBM14_586', 'GBM14_588T_M8': '', 'GBM14_591T1': 'IRCR_GBM14_591_T01', 'GBM14_593T': 'IRCR_GBM14_593', 'GBM14_594T2_M8': '', 'GBM14_605T_M8': 'IRCR_GBM14_605', 'GBM14_606T': '', 'GBM14_608T': 'IRCR_GBM14_608', 'GBM14_617T': 'IRCR_GBM14_617', 'GBM14_619T': 'IRCR_GBM14_619_T01', 'GBM14_629T': 'IRCR_GBM14_629', 'GBM14_664T1': 'IRCR_GBM14_664_T01', 'GBM14_664T2_M9': 'IRCR_GBM14_664_T02', 'GBM14_665T1': 'IRCR_GBM14_665_T01', 'GBM14_669T': '', 'GBM15_677T': 'IRCR_GBM15_677', 'GBM15_680T': 'IRCR_GBM15_680', 'GBM15_682T': 'IRCR_GBM15_682', 'GBM15_689T': '', 'GBM15_693T1': 'IRCR_GBM15_693_T01', 'GBM15_693T2': 'IRCR_GBM15_693_T02', 'GBM15_693T4': 'IRCR_GBM15_693_T04', 'GBM15_694T2': 'IRCR_GBM15_694_T02', 'GBM15_694T3': 'IRCR_GBM15_694_T03', 'GBM15_694T5': 'IRCR_GBM15_694_T05', 'GBM15_696T': 'IRCR_GBM15_696', 'GBM15_698T': 'IRCR_GBM15_698', 'GBM15_699T': 'IRCR_GBM15_699', 'GBM15_700T': 'IRCR_GBM15_700', 'GBM15_705T': 'IRCR_GBM15_705', 'GBM15_708T': 'IRCR_GBM15_708_TA', 'GBM15_709T1_M8': 'IRCR_GBM15_709_T01', 'GBM15_714T_M9': '', 'GBM15_717T': '', 'GBM15_718T1': '', 'GBM15_718T2': '', 'GBM15_729T': '', 'GBM15_732T_M8': '', 'GBM15_734T2_M8': '', 'GBM15_756T_M8': '', 'GBM15_757T2_M8': '', 'GBM15_758T_M8': ''}

def main(inDrugFileName,outDirName,outFileName,geneL='wg',cutoff=0.05, plottype='AUC', plot='FALSE', outPlotDirName='/home/heejin/DrugScreening/figure',seqType='WES'):

	if seqType == 'WES':
		idH = WESidH
	else:
		idH = WTSidH

	inFile = open(inDrugFileName)

	drugH = {}

	drugL = inFile.readline()[:-2].split(',')[1:]

	for drug in drugL:

		drugH[drug] = {}

	for line in inFile:
		
		dataH = {}

		dataL = line[:-2].split(',')

		sId = dataL[0]

		for i in range(len(drugL)):
			dataH[sId] = dataL[i+1]
			drugH[drugL[i]].update(dataH)


	con,cursor = mymysql.connectDB(db='common')

	if geneL == 'wg':
		cursor.execute('SELECT distinct geneName FROM refFlat_hg19')
		geneL = [x for (x,) in cursor.fetchall()]
	elif geneL == 'cs':
		cursor.execute('SELECT distinct gene_sym FROM cs_gene')
		geneL = [x for (x,) in cursor.fetchall()]
	else:
		geneL = geneL


	# mutation
	
	outFile = open(outFileName, 'w')
	outFile.write('Drug\tGene\tp_twosided\tp_greater\tp_less\tD\tp_twosided2\tD2\twtN\tmutN\twt_sampN\tmut_sampN\twilcox_p\tttest_p\tmed_z.score\tmean_z.score\tAltInfo\n')
	outFile.close()

	con,cursor = mymysql.connectDB(db='ircr1')

	dbIdL = idH.values()

	cursor.execute('select distinct samp_id from mutation_rxsq where nReads_alt >0 and n_nReads_ref>0')
	procSampL = [x for (x,) in cursor.fetchall()]

	for gN in geneL:

		tempFileName = '%s/temp4test.txt' % outDirName
		tempFile = open(tempFileName, 'w')

		tempFile.write('Drug\tGene\tds_id\tdb_id\tAUC\tAlt\n')

		cursor.execute('SELECT samp_id,gene_symL,ch_aa,ch_type,nReads_alt/(nReads_ref+nReads_alt) as maf FROM mutation_rxsq \
			where gene_symL ="%s" and nReads_alt>2 and ch_type not like "%ssilent%s" and ch_type not like "%ssyn%s" and \
			(ch_aa <>"" or ch_type like "%ssplice%s")' % (gN,'%','%','%','%','%','%'))
		result = cursor.fetchall()

		mutH = {}
		
		if len(result) == 0:
			continue

		for (dbId, gs, aa, type, maf) in result:
			try:
				if float(maf) < cutoff:
					continue
			except:
				continue

			mybasic.addHash(mutH,dbId,(type,maf,aa))
			#mutH[dbId] = (type,maf,aa)			
		
		scr_idL = drugH[drugH.keys()[0]].keys()	
		
		for drug in drugH.keys():
		
			for id in idH.keys():
		
				if id not in scr_idL:
					continue

				if idH[id] not in procSampL:
					continue

				try:
					Alt = mutH[idH[id]]
					Alt = '/'.join(map(str,Alt))
				except:
					Alt = 'NA'

				tempFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (drug, gN, id, idH[id], drugH[drug][id], Alt))

		tempFile.close()
		os.system('Rscript ~/JK1/NSL/HTS/drugRespByAlt2.R %s %s %s %s %s' % (tempFileName, outFileName,plot,outPlotDirName,plottype))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])

optH = mybasic.parseParam(optL)

main('/home/heejin/DrugScreening/Input/150409_AUC_v4.csv','/home/heejin/DrugScreening/','/home/heejin/DrugScreening/result_AUC_QC_v4_f20_type.txt',geneL='cs',cutoff=0.20,plottype='AUC',plot='TRUE', outPlotDirName = '/home/heejin/DrugScreening/figure/MUTv4_type',seqType='WES')

