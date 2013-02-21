#!/usr/bin/python

import os,re
import mybasic,sys,getopt

optL, argL = getopt.getopt(sys.argv[1:],'i:j:k:f:',[])

optH = mybasic.parseParam(optL)

barcode_sample=optH['-i']
gene_names=optH['-j']
geneseq=optH['-k']


#sample dictionary
sample={}
for line in open(barcode_sample):
	sample.update({line[:-2].split('\t')[0]:line[:-2].split('\t')[1]})	

genename=[]
for line in open(gene_names):
	genename.append(line[:-2])
sequences=[]
for line in open(geneseq):
	sequences.append(line[:-2])

#gene dictionary
gene={}
for i in range(len(genename)):
	tempdict={sequences[i]:genename[i]}
	gene.update(tempdict)

namelist=[]
for i in sample.items():
	namelist.append(i[1])

#'data'
data={}
for names in namelist:
	tempdict2={names:{}}
	data.update(tempdict2)
	for i in range(len(genename)):
		tempdict3={genename[i]:0}
		data[names].update(tempdict3)

f=os.popen('cat /EQL1/NSL/Barcode/464_827_Pool_1T_Barcode_*.fastq','r')

#####pattern
pattern=re.compile('([ACTGN]{4})[ACTGN]{2}ACAT[ATCGN]{15}([ATCGN]{8})[ATCGN]{68}')

count=0
iter=0
success=0
for line in f:
	count+=1
	if count%4==2:
		iter+=1
		match=re.match(pattern,line)
		if match!=None and sample.has_key(match.group(1)) and gene.has_key(match.group(2)):
			success+=1
			data[sample[match.group(1)]][gene[match.group(2)]]+=1
f.close()

resultfile=open('resultfile.txt','w')

for sampleN in data:
        for geneN in data[sampleN]:
                resultfile.write('%s\t%s\t%s\n'%(sampleN,geneN,data[sampleN][geneN]))

resultfile.close()

rate=float(success)/iter*2

print rate
print iter
print success
