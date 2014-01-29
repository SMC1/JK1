## system-wide configurations

ucscSeqDir = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18', 'hg19': '/data1/Sequence/ucsc_hg19'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X', 'hg19': '/Z/Sequence/ucsc_hg19'}}
refFlatH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'}, 'smc2': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/Z/Sequence/ucsc_hg19/annot/refFlat.txt'}}
dbsnpH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/Z/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}}
ucscRefH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fasta'}}
bwaIndexH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fa'}}
SGI_PATH = {'hiseq1':'119.5.134.125:/BiO', 'hiseq2':'119.5.134.126:/BiO'}
SGI_DIR_PREFIX = {'hiseq1':'/EQL2/sgi_hiseq1','hiseq2':'/EQL2/sgi_hiseq2'}
mysqlH={'smc1':{'user':'cancer','passwd':'cancer','host':'localhost'}, 'smc2':{'user':'cancer','passwd':'cancer','host':'119.5.134.165'}}
wxsBamDirL = ['/EQL3/pipeline/SGI20131031_xsq2mut','/EQL3/pipeline/SGI20131119_xsq2mut/','/EQL3/pipeline/SGI20131212_xsq2mut/', '/EQL3/pipeline/SGI20131216_xsq2mut/', '/EQL3/pipeline/SGI20140103_xsq2mut','/EQL3/pipeline/somatic_mutect/']
## list of samples to be used as pooled normal for CNA (for wxs from DNA Link)
cnaBaseDir = '/EQL3/pipeline/CNA'
poolB_DLink = []
for dir in ['S012_T_SS','S023_T_SS','S025_T_TS','S042_T_SS','S047_T_SS','S050_T_SS','S092_T_SS','S179_T_SS','S464_T_SS','S520_T_SS','S532_T_SS','S538_T_SS','S567_T_SS','S586_T_SS','S626_T_SS','S640_T_SS']:
	poolB_DLink.append(cnaBaseDir + '/' + dir)
## list of samples to be used as pooled normal for CNA (for wxs from SGI)
poolB_SGI = []
for dir in ['S3A_T_SS','S5A_T_SS','S7A_T_SS','S8A_T_SS','S9A_T_SS','S10A_T_SS','S11A_T_SS','S12A_T_SS','S14A_T_SS','S722_T_SS','S171_T_SS','S121_T_SS','S208_T_SS','S223_T_SS','S240_T_SS','S243_T_SS','S323_T_SS']:
	poolB_SGI.append(cnaBaseDir + '/' + dir)
