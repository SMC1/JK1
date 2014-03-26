## system-wide configurations

ucscSeqDir = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18', 'hg19': '/data1/Sequence/ucsc_hg19'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X', 'hg19': '/Z/Sequence/ucsc_hg19'}}
refFlatH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'}, 'smc2': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/Z/Sequence/ucsc_hg19/annot/refFlat.txt'}}
refSeqBed12H = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/hg19_refSeq.bed12'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/hg19_refSeq.bed12'}}
dbsnpH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/Z/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}}
ucscRefH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fasta'}}
bwaIndexH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fa'}}
SGI_PATH = {'hiseq1':'119.5.134.125:/BiO/Unaligned_Fastq', 'hiseq2':'119.5.134.126:/BiO/Unaligned_Fastq'}
SGI_DIR_PREFIX = {'hiseq1':'/EQL2/sgi_hiseq1','hiseq2':'/EQL2/sgi_hiseq2'}
mysqlH={'smc1':{'user':'cancer','passwd':'cancer','host':'localhost'}, 'smc2':{'user':'cancer','passwd':'cancer','host':'119.5.134.165'}}
wxsBamDirL = ['/EQL2/pipeline/SGI20140219_xsq2mut','/EQL2/pipeline/SGI20140210_xsq2mut','/EQL2/pipeline/SGI20140204_xsq2mut','/EQL2/pipeline/SGI20140128_xsq2mut','/EQL3/pipeline/SGI20140103_xsq2mut','/EQL3/pipeline/SGI20131216_xsq2mut/','/EQL3/pipeline/SGI20131212_xsq2mut/','/EQL3/pipeline/SGI20131119_xsq2mut/','/EQL3/pipeline/SGI20131031_xsq2mut','/EQL3/pipeline/somatic_mutect/']
oldPipelineL = ['/EQL1/NSL/WXS/exome_20130529','/EQL1/pipeline/ExomeSeq_20130723']
wxsPileupDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/pileup_link']
wxsPileupProcDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/pileup_proc']
wxsMutscanDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/mutscan']
rsqPipelineDirL = ['/EQL2/pipeline/SGI20140204_rsq2mut','/EQL3/pipeline/SGI20131226_rsq2mut','/EQL1/pipeline/SGI20131212_rsq2mut','/EQL1/pipeline/SGI20131119_rsq2mut','/EQL1/pipeline/SGI20131031_rsq2mut']
oldRsqDirL = ['/EQL1/NSL/RNASeq/alignment/splice_Z/gatk_test','/EQL1/pipeline/RNAseq_mut_096_145','/EQL1/pipeline/RNAseq_mut_PR','/EQL1/pipeline/RNAseq_17','/EQL1/pipeline/RNAseq_mut_FGFR', '/EQL1/pipeline/RNAseq_mut_15']
rsqMutscanDirL = rsqPipelineDirL + oldRsqDirL
## list of samples to be used as pooled normal for CNA (for wxs from DNA Link)
cnaBaseDir = '/EQL3/pipeline/CNA'
poolB_DLink = []
for dir in ['S012_T_SS','S023_T_SS','S025_T_TS','S042_T_SS','S047_T_SS','S050_T_SS','S092_T_SS','S179_T_SS','S464_T_SS','S520_T_SS','S532_T_SS','S538_T_SS','S567_T_SS','S586_T_SS','S626_T_SS','S640_T_SS']:
	poolB_DLink.append(cnaBaseDir + '/' + dir)
## list of samples to be used as pooled normal for CNA (for wxs from SGI)
poolB_SGI = []
for dir in ['S3A_T_SS','S5A_T_SS','S7A_T_SS','S8A_T_SS','S9A_T_SS','S10A_T_SS','S11A_T_SS','S12A_T_SS','S14A_T_SS','S796_T_SS','S171_T_SS','S121_T_SS','S208_T_SS','S223_T_SS','S240_T_SS','S243_T_SS','S323_T_SS','S015_T_SS','S386_T_SS','S723_T_SS']:
	poolB_SGI.append(cnaBaseDir + '/' + dir)
poolB_DLink_bam='/EQL1/NSL/WXS/results/CNA/DLink_B_pool.recal.bam' ## 'recal' is added without actual recalibration
poolB_SGI_bam='/EQL1/NSL/WXS/results/CNA/SGI_B_pool.recal.bam' ## 'recal' is added without actual recalibration
