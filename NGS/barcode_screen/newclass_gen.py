#!/usr/bin/python

import os,re
import mybasic,sys,getopt

optL, argL = getopt.getopt(sys.argv[1:],'i:j:k:f:r:',[])

optH = mybasic.parseParam(optL)

barcode_sample=optH['-i']
gene_names=optH['-j']
geneseq=optH['-k']
fastqname=optH['-f']
resultname=optH['-r']

#sample dictionary 생성
sample={}
for line in open(barcode_sample):
	sample.update({line[:-1].split('\t')[0]:line[:-1].split('\t')[1]})	

#gene의 이름을 나열한 'genename' list 형성. 차후에 gene sequence에 gene의 이름을 할당한 dictionary를 생성하기 위해 필요
genename=[]
for line in open(gene_names):
	genename.append(line[:-1])
#genename과 동일한 순서로 sequence를 나열한 'sequences' list 형성
sequences=[]
for line in open(geneseq):
	sequences.append(line[:-1])

#gene dictionary 생성
gene={}
for i in range(len(genename)):
	tempdict={sequences[i]:genename[i]}
	gene.update(tempdict)

#sample의 이름을 나열한 list 'namelist'생성
#최종 output dictionary인 'data'를 생성하기 위한 것
namelist=[]
for i in sample.items():
	namelist.append(i[1])

#'data'생성
#key로 namelist의 sample name 사용
#각 sample name에 gene별 count를 위한 새로운 dictionary 할당
data={}
for names in namelist:
	tempdict2={names:{}}
	data.update(tempdict2)
	for i in range(len(genename)):
		tempdict3={genename[i]:0}
		data[names].update(tempdict3)

#파일 stream 형태로 open
f=os.popen('cat %s'%fastqname,'r')

#####pattern 을 re 패키지의 compile함수를 이용하여 생성 
pattern=re.compile('([ACTGN]{3})([ACTGN]{3})ACAT[ATCGN]{15}([ATCGN]{8})[ATCGN]{3}([ATCGN]{8})[ATCGN]{57}')

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
			data[sample[match.group(1)]][gene[match.group(3)]]+=1
f.close()

resultfile=open('%s.txt'%resultname,'w')

for sampleN in data:
        for geneN in data[sampleN]:
                resultfile.write('%s\t%s\t%s\n'%(sampleN,geneN,data[sampleN][geneN]))

resultfile.close()

#전체 데이터에 대한 gene matching 성공 비율 산출 
rate=float(success)/iter*2

print rate

