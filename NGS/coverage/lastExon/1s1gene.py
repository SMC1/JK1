import sys, getopt
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

bedgraph=open(bedgraphFileN,'r')
refFlat=mygenome.loadRefFlatByChr(refFlatFileN)

temp=0 
for line in bedgraph:
	l=line.split('\t')
	chr_sample=l[0]
	if (chr_sample!='chr7' and temp==1):
		break
	if chr_sample=='chr7' and refFlat.has_key(chr_sample):
		s=int(l[1])
		e=int(l[2])
		d=int(l[3])
		temp=1  
		for gene in refFlat[chr_sample]:
			GeneN=gene['geneName']
			if not data.has_key(GeneN):
				data.update({GeneN:{}})
			SeqId=gene['refSeqId']
			if not data[GeneN].has_key(SeqId):
				data[GeneN].update({SeqId:{'denominator':0,'nominator':0,'rate':0}})
			if not (e<gene['exnList'][0][0] or s>gene['exnList'][len(gene['exnList'])-1][1]):
				for exon in gene['exnList']:
					length=overlap((s,e),(exon[0],exon[1]))
					if length!=0:
						dens=length*d
						data[GeneN][SeqId]['denominator']+=dens
						if exon==gene['exnList'][len(gene['exnList'])-1]:
							data[GeneN][SeqId]['nominator']+=dens

fo=open('%s_lastExon.txt'%(filePathPrefix),'w')
fo.write('%s\n'%(filePathPrefix))
for GN in data:
	for SId in data[GN]:
		if data[GN][SId]['denominator']!=0:
			data[GN][SId]['rate']=float(data[GN][SId]['nominator'])/data[GN][SId]['denominator']
			fo.write('%s\t%s\t%s\n'%(GN,SId,data[GN][SId]['rate']))
		else:
			fo.write('%s\n'%('denominator=0'))
fo.close()




