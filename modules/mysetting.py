## system-wide configurations

from glob import glob

ucscSeqDir = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18', 'hg19': '/data1/Sequence/ucsc_hg19'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X', 'hg19': '/Z/Sequence/ucsc_hg19'}}
refFlatH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'}, 'smc2': {'hg18': '/data1/Sequence/ucsc_hg18/annot/refFlat_hg18.txt', 'hg19': '/Z/Sequence/ucsc_hg19/annot/refFlat.txt'}}
refSeqBed12H = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/hg19_refSeq.bed12'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/hg19_refSeq.bed12'}}
dbsnpH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/annot/dbsnp_132.hg18.sorted.vcf', 'hg19': '/Z/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'}}
all_1kgH = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/ALL.wgs.phase1_release_v3.20101123.snps_indels_sv.sites.hg19.vcf'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/ALL.wgs.phase1_release_v3.20101123.snps_indels_sv.sites.hg19.vcf'}}
espH = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/ESP6500SI-V2-SSA137.updatedProteinHgvs.ALL.snps_indels.hg19.vcf'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/ESP6500SI-V2-SSA137.updatedProteinHgvs.ALL.snps_indels.hg19.vcf'}}
indel_1kgH = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/1000G_phase1.indels.hg19.reorder.vcf'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/1000G_phase1.indels.hg19.reorder.vcf'}}
indel_gsH = {'smc1': {'hg19': '/data1/Sequence/ucsc_hg19/annot/Mills_and_1000G_gold_standard.indels.hg19.vcf'}, 'smc2': {'hg19': '/Z/Sequence/ucsc_hg19/annot/Mills_and_1000G_gold_standard.indels.hg19.vcf'}}
cosmicH = {'smc1': {'hg19': '/data1/Sequence/cosmic/hg19_cosmic_v54_120711.vcf'}, 'smc2': {'hg19': '/Z/Sequence/cosmic/hg19_cosmic_v54_120711.vcf'}}
ucscRefH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fasta'}}
bwaIndexH = {'smc1': {'hg18': '/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19': '/data1/Sequence/ucsc_hg19/hg19.fa'}, 'smc2': {'hg18': '/Z/Sequence/ucsc_hg18X/hg18.fa', 'hg19': '/Z/Sequence/ucsc_hg19/hg19.fa'}}
SGI_PATH = {'hiseq1':'119.5.134.125:/BiO/Unaligned_Fastq', 'hiseq2':'119.5.134.126:/BiO/Unaligned_Fastq'}
SGI_DIR_PREFIX = {'hiseq1':'/EQL2/sgi_hiseq1','hiseq2':'/EQL2/sgi_hiseq2'}
mysqlH={'smc1':{'user':'cancer','passwd':'cancer','host':'localhost'}, 'smc2':{'user':'cancer','passwd':'cancer','host':'119.5.134.165'}}
wxsBamDirL = glob('/EQL2/pipeline/SGI*xsq2mut') + glob('/EQL3/pipeline/SGI*xsq2mut') + ['/EQL3/pipeline/somatic_mutect']
oldPipelineL = ['/EQL1/NSL/WXS/exome_20130529','/EQL1/pipeline/ExomeSeq_20130723']
wxsPileupDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/pileup_link']
wxsPileupProcDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/pileup_proc']
wxsMutscanDirL = wxsBamDirL + oldPipelineL + ['/EQL1/NSL/exome_bam/mutation/mutscan']
wxsMutectDir='/EQL3/pipeline/somatic_mutect'
wxsCNADir='/EQL3/pipeline/CNA'
wxsPurityDir='/EQL3/pipeline/Purity'
wxsCNAcorrDir='/EQL3/pipeline/CNA_corr'
wxsClonalityDir='/EQL3/pipeline/Clonality'
rsqPipelineDirL = ['/EQL2/pipeline/SGI20140204_rsq2mut','/EQL3/pipeline/SGI20131226_rsq2mut','/EQL1/pipeline/SGI20131212_rsq2mut','/EQL1/pipeline/SGI20131119_rsq2mut','/EQL1/pipeline/SGI20131031_rsq2mut']
oldRsqDirL = ['/EQL1/NSL/RNASeq/alignment/splice_Z/gatk_test','/EQL1/pipeline/RNAseq_mut_096_145','/EQL1/pipeline/RNAseq_mut_PR','/EQL1/pipeline/RNAseq_17','/EQL1/pipeline/RNAseq_mut_FGFR', '/EQL1/pipeline/RNAseq_mut_15']
rsqMutscanDirL = rsqPipelineDirL + oldRsqDirL
rsqBedDirL = glob('/EQL1/pipeline/*rsq2expr') + glob('/EQL2/pipeline/*rsq2expr') + glob('/EQL3/pipeline/*rsq2expr') + ['/EQL1/pipeline/RNAseq_expr_096_145','/EQL1/pipeline/RNAseq_expr_FGFR','/EQL1/NSL/RNASeq/coverage'] #bed files are in [dir]/*/*bed
cnaBaseDir = '/EQL3/pipeline/CNA'
## list of samples to be used as pooled normal for CNA (for wxs from DNA Link)
poolB_DLink = []
for dir in ['S042_T_SS','S047_T_SS','S050_T_SS','S140_T_SS','S464_T_SS','S532_T_SS','S567_T_SS','S586_T_SS','S602_T_SS','S626_T_SS','S697_T_SS','S768_T_SS','S773_T_SS','S788_T_SS']:
	poolB_DLink.append(wxsCNADir + '/' + dir)
## list of samples to be used as pooled normal for CNA (for wxs from SGI)
poolB_SGI = []
#for dir in ['S3A_T_SS','S5A_T_SS','S7A_T_SS','S8A_T_SS','S9A_T_SS','S10A_T_SS','S11A_T_SS','S12A_T_SS','S14A_T_SS','S796_T_SS','S171_T_SS','S121_T_SS','S208_T_SS','S223_T_SS','S240_T_SS','S243_T_SS','S323_T_SS','S015_T_SS','S386_T_SS','S723_T_SS']:
for dir in ['S015_T_SS','S208_T_SS','S223_T_SS','S240_T_SS','S320_T_SS','S334_T_SS','S335_T_SS','S386_T_SS','S388_T_SS','S470_T_SS','S723_T_SS','IRCR_GBM_363_TM_SS']:
	poolB_SGI.append(wxsCNADir + '/' + dir)
poolB_DLink_bam='/EQL1/NSL/WXS/results/CNA/DLink_B_pool.recal.bam' ## 'recal' is added without actual recalibration
poolB_SGI_bam='/EQL1/NSL/WXS/results/CNA/SGI_B_pool.recal.bam' ## 'recal' is added without actual recalibration
poolB_CS_bam='/EQL1/NSL/WXS/results/CNA/CS_B_pool.recal.bam' ## for cancerscan (from 20 hapmap)
poolB_CS_rpkm='/EQL1/NSL/WXS/results/CNA/CS_B_pool.rpkm' ## for cancerscan (from 20 hapmap)
#cancerscan genes (copy to Integration/cgi/ircr_samp.py, Integration/cgi/oncoprint.py)
cs_gene = ['ABL1','AKT1','AKT2','AKT3','ALK','APC','ARID1A','ARID1B','ARID2','ATM','ATRX','AURKA','AURKB','BCL2','BRAF','BRCA1','BRCA2','CDH1','CDK4','CDK6','CDKN2A','CSF1R','CTNNB1','DDR2','EGFR','EPHB4','ERBB2','ERBB3','ERBB4','EWSR1','EZH2','FBXW7','FGFR1','FGFR2','FGFR3','FLT3','GNA11','GNAQ','GNAS','HNF1A','HRAS','IDH1','IDH2','IGF1R','ITK','JAK1','JAK2','JAK3','KDR','KIT','KRAS','MDM2','MET','MLH1','MPL','MTOR','NF1','NOTCH1','NPM1','NRAS','NTRK1','PDGFRA','PDGFRB','PIK3CA','PIK3R1','PTCH1','PTCH2','PTEN','PTPN11','RB1','RET','ROS1','SMAD4','SMARCB1','SMO','SRC','STK11','SYK','TMPRSS2','TOP1','TP53','VHL']
