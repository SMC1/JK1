drop table IF EXISTS drugbank;
CREATE TABLE drugbank (
	drug text NOT NULL,
	gene_sym varchar(31) NOT NULL
);

/*LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_cn/TCGA_GBM_CNA_SNP6_tumorOnly.dat" INTO TABLE array_cn;*/
LOAD DATA LOCAL INFILE "/home/heejin/druginfo/druginfo_ft.txt" INTO TABLE drugbank;
