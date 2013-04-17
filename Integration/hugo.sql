drop table IF EXISTS hugo;
CREATE TABLE hugo (
	gene_sym varchar(31) NOT NULL,
	gene_desc text,
	prev_sym text,
	synonyms text,
	refSeq_id varchar(31),
	primary key (gene_sym)
);

/*LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_cn/TCGA_GBM_CNA_SNP6_tumorOnly.dat" INTO TABLE array_cn;*/
LOAD DATA LOCAL INFILE "/data1/Sequence/geneinfo/hugo.txt" INTO TABLE hugo;
