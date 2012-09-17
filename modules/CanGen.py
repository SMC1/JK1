#!/usr/bin/python_epd

import sys, os, re, math, numpy


colorH = {False:'r',True:'g'}
mSize = {False:2, True: 3}

normalSampleCodeL = map(str,range(10,20))

clinParamNameL = ['age','prog','recur','death','censor']

regExprH = {'NSL_GBM31':'.*([0-9]{3})(T|_tissue)', 'Rembrandt_GBM':'^0*([^_]*).*', 'TCGA_GBM_BI':'(.*)', 'TCGA_GBM_UNC':'(.*)'}


class individual:

	repExonProbesetH = {}

	def __init__(self,sId,pId=''):

		self.expr = {}
		self.methyl = {}
		self.sId = sId 
		self.copyNum = {}
		self.pId = pId
		self.exonExpr = {}
		self.age = -1
		self.prog = -1
		self.recur = -1
		self.death = -1
		self.censor = -1
		self.es = {}
		self.pred = {}
		self.pheno = {}

		if pId == '':
			self.pId = sId[:-3]
		

	def isNormal(self):

		return self.sId[13:15] in normalSampleCodeL

	def setClinical(self,paramL):

		for i in range(5):
			if paramL[i] != -1:
				setattr(self, clinParamNameL[i], paramL[i])

	def setEs(self,gsetName,es,pval):

		self.es[gsetName] = (es,pval)

	def setPred(self,predName,classCode,fdr,dist):

		self.pred[predName] = (classCode,fdr,dist)

	def setPheno(self,phenoName,phenoCode,phenoLabel):

		self.pheno[phenoName] = (phenoCode,phenoLabel)

	def setExpr(self,platform,geneName,value):

		if platform in self.expr:
			self.expr[platform][geneName] = float(value)
		else:
			self.expr[platform] = {geneName:float(value)}

	def setMethyl(self,geneName,locus,value):

		if geneName in self.methyl:
			self.methyl[geneName][locus] = value
		else:
			self.methyl[geneName] = {locus:value}

	def setCopyNum(self,plat,geneName,frac,value):

		mybio.addMultiLevelHash(self.copyNum,(plat,geneName),(frac,value))

	def setExonExpr(self,geneName,exon,probesetId,value):

		mybio.setMultiLevelHash(self.exonExpr,[geneName,exon,probesetId],value)

	def getExpr(self,geneName,plat):

		return self.expr[plat][geneName]

	def getPred(self,predName):

		return self.pred[predName]

	def getEs(self,GSetName):

		return self.es[GsetName]

	def getPheno(self,phenoName):

		return self.pheno[phenoName]

	def getMethyl(self,geneName):

		return numpy.mean(self.methyl[geneName].values())

	def getCopyNum(self,geneName,(plat,indH,normalize)):

		if normalize == True:

			if self.isNormal():
				raise Exception

			ind_normL = filter(lambda x: x.sId[:-2]==self.sId[:-2] and x.sId[-2:] in normalSampleCodeL, indH.values())

			return self.getCopyNum(geneName,(plat,indH,False)) - indH[ind_normL[0].sId].getCopyNum(geneName,(plat,indH,False))

		else:

			wCN = 0.

			for (frac,value) in self.copyNum[plat][geneName]:
				wCN += frac * value

			return wCN


	def getExonExpr(self,geneName,exon):

		return self.exonExpr[geneName][exon]

	def getAge(self):
		
		return self.age

	def getProg(self):
		
		return self.prog

	def getRecur(self):
		
		return self.recur

	def getDeath(self):
		
		return self.death

	def getCensor(self):
		
		return self.censor


def loadGct(indH,geneNameL,filePath,plat='NA',sNameRegExpr='(.*)'):

	inFile = open(filePath)
	inFile.readline()
	inFile.readline()

	headerTok = inFile.readline()[:-1].split('\t')

	sIdL = [re.search(sNameRegExpr,t).group(1) for t in headerTok[2:]]

	indH_keys = indH.keys()

	for line in inFile:

		tok = line[:-1].split('\t')

		geneName = tok[0].upper()

		if not geneName in geneNameL:
			continue

		for i in range(2,len(tok)):

			sId = sIdL[i-2]

			if not sId in indH_keys:
				indH[sId] = individual(sId)

			value = tok[i]

			if value in ('NA','null','NULL'):
				continue

			indH[sId].setExpr(plat,geneName,float(value))

	return indH


def loadPheno(indH,phenoName,phenoH):

	indH_keys = indH.keys()

	ind2label = {}

	for ((phenoCode,phenoLabel),sIdL) in phenoH.items():

		for sId in sIdL:

			if not sId in indH_keys:
				indH[sId] = individual(sId,sId)

			indH[sId].setPheno(phenoName,phenoCode,phenoLabel)

			ind2label[indH[sId]] = (phenoLabel,phenoCode)

	return (indH, ind2label)
		

def loadPred(indH, predName, filePath, regExpr='(.*)'):

	inFile = open(filePath)
	inFile.readline()

	indH_keys = indH.keys()

	indIdL_old = []; indIdL_new = []

	for line in inFile:

		tokL = line[:-1].split('\t')

		pId = re.match(regExpr, tokL[0]).group(1)

		classCode = int(tokL[1])
		rank = float(tokL[3])
		fdr = float(tokL[5])

		if classCode==1:
			dist = float(tokL[2])
		else:
			dist = 2-float(tokL[2])

		if not pId in indH_keys:
			indH[pId] = individual(pId)
			indIdL_new.append(pId)
		else:
			indIdL_old.append(pId)

		indH[pId].setPred(predName,classCode,fdr,dist)

	print '\n[loadPred]:', predName
	print 'Pre-existing:', len(indIdL_old), indIdL_old
	print 'Newly-entered:', len(indIdL_new), indIdL_new

	return indH


def loadES(indH, gsetName, filePath, regExpr='(.*)'):

	inFile = open(filePath)

	indH_keys = indH.keys()

	for line in inFile:

		tokL = line[:-1].split('\t')

		sId = re.match(regExpr, tokL[0]).group(1)
		es = float(tokL[1])
		es_pval = float(tokL[2])

		if not sId in indH_keys:
			indH[sId] = individual(sId)

		indH[sId].setEs(gsetName,es,es_pval)

	return indH


def loadClinical(indH,filePath,regExpr='(.*)'):

	inFile = open(filePath)
	inFile.readline()

	indH_keys = indH.keys()

	indIdL_old = []; indIdL_new = []

	for line in inFile:

		tokL = line[:-1].split('\t')

		rm = re.search(regExpr,tokL[0])

		if rm:

			pId = rm.group(1)

			if not pId in indH_keys:
				indH[pId] = individual(sId=pId,pId=pId)
				indIdL_new.append(pId)
			else:
				indIdL_old.append(pId)

			age = int(tokL[1])
			death = float(tokL[3])
			followup = max(float(tokL[4]),death)
			
			if len(tokL) >= 6:
				prog = float(tokL[5])
			else:
				prog = -1

			indH[pId].setClinical([age,prog,-1,death,followup])

	print '\n[loadClinical]:'
	print 'Pre-existing:', len(indIdL_old), indIdL_old
	print 'Newly-entered:', len(indIdL_new), indIdL_new

	return indH


def selectCol(colGrpH, dataDir, dataName, regExpr='^%s$', flag=True):

	grpNameL = colGrpH.keys()
	grpNameL.sort()

	inGctFile = open('%s/%s.gct' % (dataDir,dataName))

	inGctFile.readline()
	(nRow,nCol) = gctRowCol(inGctFile.readline())
	headerTokL = inGctFile.readline().rstrip().split('\t')

	idxH = {}
	nSample = 0

	for gN in grpNameL:

		idxH[gN] = []

		for s in colGrpH[gN]:

			for i in range(2,len(headerTokL)):

				rE = regExpr % s
				rm = re.match(rE, headerTokL[i])

				if rm:
					nSample += 1
					idxH[gN].append(i)
					break

	outGctFile = open('%s/%s_%s.gct' % (dataDir,dataName,nSample), 'w')

	outGctFile.write('#1.2\n%s\t%s\n' % (nRow,nSample))

	newHeaderTokL = []
	
	for gN in grpNameL:

		tempL = np.array(headerTokL).take(idxH[gN])

		if flag:
			newHeaderTokL += map(lambda x: '%s_%s' % (gN[0],x), tempL)
		else:
			newHeaderTokL += map(lambda x: x, tempL)

	outGctFile.write('%s\t%s\t%s\n' % ('NAME', 'Description', '\t'.join(newHeaderTokL)))

	for line in inGctFile:

		tokL = line[:-1].split('\t')

		newTokL = []
		
		for gN in grpNameL:
			newTokL += np.array(tokL).take(idxH[gN])

		outGctFile.write('%s\t%s\t%s\n' % (tokL[0],tokL[1], '\t'.join(newTokL)))

	outClsFile = open('%s/%s_%s.cls' % (dataDir,dataName,nSample),'w')

	outClsFile.write('%s\t%s\t1\n' % (nSample,len(idxH)))

	outClsFile.write('# %s\n' % ' '.join([gN[1] for gN in grpNameL]))

	tokL = []
	
	for gN in grpNameL:
		tokL += ['%s' % (gN[0]-1,),] * len(idxH[gN])

	outClsFile.write('%s' % ' '.join(tokL))


def survival(indL, fun, ind2label, outDir, criteria, dataName, attrL = ['death']):

	for attr in attrL:

		outFile = open('%s/survival_%s_%s.txt' % (outDir,criteria,attr), 'w')
		outFile.write('id\tvalue\tlabelTxt\tlabelNum\tevent\ttime\n')

		for ind in indL:

			value = apply(fun,(ind,))
			label = ind2label[ind]
			time = getattr(ind,'get'+attr[0].upper()+attr[1:])()
			followup = ind.getCensor()

			if time > 0:
				outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (ind.pId,value,label[0],label[1],1,time))
			elif followup > 0:
				outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (ind.pId,value,label[0],label[1],0,followup))

		outFile.close()

		os.system('/usr/bin/Rscript %s/survival.r %s %s_%s %s' % (codeDir,outDir,criteria.replace('$','\$'),attr,dataName))

