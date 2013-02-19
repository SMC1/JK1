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

#sample dictionary ����
sample={}
for line in open(barcode_sample):
	sample.update({line[:-1].split('\t')[0]:line[:-1].split('\t')[1]})	

#gene�� �̸��� ������ 'genename' list ����. ���Ŀ� gene sequence�� gene�� �̸��� �Ҵ��� dictionary�� �����ϱ� ���� �ʿ�
genename=[]
for line in open(gene_names):
	genename.append(line[:-1])
#genename�� ������ ������ sequence�� ������ 'sequences' list ����
sequences=[]
for line in open(geneseq):
	sequences.append(line[:-1])

#gene dictionary ����
gene={}
for i in range(len(genename)):
	tempdict={sequences[i]:genename[i]}
	gene.update(tempdict)

#sample�� �̸��� ������ list 'namelist'����
#���� output dictionary�� 'data'�� �����ϱ� ���� ��
namelist=[]
for i in sample.items():
	namelist.append(i[1])

#'data'����
#key�� namelist�� sample name ���
#�� sample name�� gene�� count�� ���� ���ο� dictionary �Ҵ�
data={}
for names in namelist:
	tempdict2={names:{}}
	data.update(tempdict2)
	for i in range(len(genename)):
		tempdict3={genename[i]:0}
		data[names].update(tempdict3)

#���� stream ���·� open
f=os.popen('cat %s'%fastqname,'r')

#####pattern �� re ��Ű���� compile�Լ��� �̿��Ͽ� ���� 
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

#��ü �����Ϳ� ���� gene matching ���� ���� ���� 
rate=float(success)/iter*2

print rate

