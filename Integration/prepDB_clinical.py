#!/usr/bin/python

import sys, getopt, re, numpy
import mybasic

def main(inFileName,outFileName):

	outFile = open(outFileName,'w')

	nameH = {'pId':'bcr_patient_barcode', 'pId_uuid':'bcr_patient_uuid', 'year':'year_of_initial_pathologic_diagnosis', 'age':'age_at_initial_pathologic_diagnosis', 'gender':'gender', 'days_death':'days_to_death', 'days_followup':'days_to_last_followup', 'pathology':'histological_type', 'prior_glioma':'prior_glioma', 'neoadjuvant':'history_of_neoadjuvant_treatment', 'KPS':'karnofsky_performance_score', 'KPS_time':'performance_status_scale_timing'}

	nameL = ['pId', 'pId_uuid', 'year', 'age', 'gender', 'days_death', 'days_followup', 'pathology', 'prior_glioma', 'neoadjuvant', 'KPS', 'KPS_time']

	replaceH = {'[Not Available]':'\N', 'MALE':'M', 'FEMALE':'F', 'Yes':'Y', 'No':'N', 'YES':'Y', 'NO':'N', 'Untreated primary (de novo) GBM':'primary,untreated', 'Treated primary GBM':'primary,treated', 'Glioblastoma Multiforme (GBM)':''}

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(nm, headerL.index(nameH[nm])) for nm in nameL])

	for line in inFile:

		for (k,v) in replaceH.items():
			line = line.replace(k,v)

		valueL = line[:-1].split('\t')
		resultL = []

		death = valueL[idxH['days_death']]
		followup = valueL[idxH['days_followup']]

		if (death!='\N' and followup=='\N') or (death!='\N' and followup!='\N' and int(death) > int(followup)):
			valueL[idxH['days_followup']] = valueL[idxH['days_death']]

		for nm in nameL:
			resultL.append(valueL[idxH[nm]])

		outFile.write('\t'.join(resultL)+'\n')

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/clinical/clinical_patient_gbm.txt','/EQL1/TCGA/GBM/clinical/clinical_TCGA_GBM.dat')
