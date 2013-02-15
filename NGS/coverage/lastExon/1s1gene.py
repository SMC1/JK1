import sys, getopt,re
import mybasic, mygenome

def overlap((s1,e1),(s2,e2)):

	if e2<=s1 or e1<=s2:
		return 0
	s=max(s1,s2)
	e=min(e1,e2)
	if s<e:
		return e-s
	else:
		return 0

optL, argL = getopt.getopt(sys.argv[1:],'i:j:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-j' in optH):

	print 'Usage: ./1s1gene.py -i [bedgraph file path] -j [refFlat file path]'
	sys.exit(0)

bedgraphFileN = optH['-i']
refFlatFileN=optH['-j']

data={}

filePathPrefix = bedgraphFileN.split('.bedgraph')[0]
split=filePathPrefix.split('/')
sampN = split[len(split)-1]

if 'D-' in sampN:
	DorW='D'
elif 'SOLiD' in sampN:
	DorW='W-SOLiD'
else:
	DorW='W'

bedgraph=open(bedgraphFileN,'r')
refFlat=mygenome.loadRefFlatByChr(refFlatFileN)


for line in bedgraph:
	l=line.split('\t')
	chr_sample=l[0]
	if refFlat.has_key(chr_sample):
		s=int(l[1])
		e=int(l[2])
		d=int(l[3])
		for gene in refFlat[chr_sample]:
			GeneN=gene['geneName']
			if not data.has_key(GeneN):
				data.update({GeneN:{}})
			SeqId=gene['refSeqId']
			if not data[GeneN].has_key(SeqId):
				data[GeneN].update({SeqId:{'denominator':1,'nominator':1,'rate':0}})  #pseudo-count
			if not (e<gene['exnList'][0][0] or s>gene['exnList'][len(gene['exnList'])-1][1]):
				for exon in gene['exnList']:
					length=overlap((s,e),(exon[0],exon[1]))
					if length!=0:
						dens=length*d
						data[GeneN][SeqId]['denominator']+=dens
						if gene['strand']=='+' and exon==gene['exnList'][len(gene['exnList'])-1]:
							data[GeneN][SeqId]['nominator']+=dens
						elif gene['strand']=='-' and exon==gene['exnList'][0]:
							data[GeneN][SeqId]['nominator']+=dens

fo=open('%s_all.txt'%(filePathPrefix),'w')
for GN in data:
	for SId in data[GN]:
		if data[GN][SId]['denominator']!=0:
			data[GN][SId]['rate']=float(data[GN][SId]['nominator'])/data[GN][SId]['denominator']
			fo.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(sampN,DorW,GN,SId,data[GN][SId]['nominator'],data[GN][SId]['denominator'],data[GN][SId]['rate']))
			#fo.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(sampN,GN,SId,data[GN][SId]['nominator'],data[GN][SId]['denominator'],data[GN][SId]['rate']))
		else:
			fo.write('%s\t%s\t%s\t%s\t%s\n'%(sampN,DorW,GN,SId,'denominator=0'))
			#fo.write('%s\t%s\t%s\t%s\n'%(sampN,GN,SId,'denominator=0'))

fo.close()




