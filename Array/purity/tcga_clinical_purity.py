#!/usr/bin/python

# biospecimen_slide_gbm.txt

import sys, getopt, re
import mybasic

def main(inFileName,outFileName):

	nameL = ('bcr_sample_barcode', 'bcr_slide_barcode', 'bcr_slide_uuid', 'number_proliferating_cells', 'percent_eosinophil_infiltration', 'percent_granulocyte_infiltration', 'percent_inflam_infiltration', 'percent_lymphocyte_infiltration', 'percent_monocyte_infiltration', 'percent_necrosis', 'percent_neutrophil_infiltration', 'percent_normal_cells', 'percent_stromal_cells', 'percent_tumor_cells', 'percent_tumor_nuclei', 'section_location')

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(x, headerL.index(x)) for x in nameL if x in headerL])

	outFile = open(outFileName,'w')

	outFile.write('bcr_slide_barcode\tbcr_sample_barcode\tpercent_tumor_cells\n')

	for line in inFile:

		valueL = line[:-1].split('\t')

		sId = valueL[idxH['bcr_sample_barcode']]
		slideId = value[idxH['bcr_slide_barcode']]
		tumor = valueL[idxH['percent_tumor_cells']]

		outFile.write('%s\t%s\t%s\n' % (slideId,sId,tumor))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/clinical/biospecimen_slide_gbm.txt','/EQL1/TCGA/GBM/clinical/clinical_tumor_percent.dat')
#main('/EQL1/TCGA/GBM/mutation/GBM-TP.final_analysis_set.maf')
