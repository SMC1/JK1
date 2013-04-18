drop table IF EXISTS kegg;
CREATE TABLE kegg (
	kegg_id varchar(63) NOT NULL,
	kegg_desc text,
	gene_sym varchar(31) NOT NULL,
	primary key (kegg_id,gene_sym)
);

/*LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_cn/TCGA_GBM_CNA_SNP6_tumorOnly.dat" INTO TABLE array_cn;*/
LOAD DATA LOCAL INFILE "/data1/Sequence/geneinfo/KEGG.dat" INTO TABLE kegg;
