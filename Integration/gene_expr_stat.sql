drop table IF EXISTS gene_expr_stat;
CREATE TABLE gene_expr_stat (
	gene_sym varchar(31) NOT NULL,
	q25 double NOT NULL,
	median double NOT NULL,
	q75 double NOT NULL,
	mean double NOT NULL,
	std_dev double NOT NULL,
	primary key (gene_sym),
	index (gene_sym)
);

/*LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_cn/TCGA_GBM_CNA_SNP6_tumorOnly.dat" INTO TABLE array_cn;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_madNorm_stat.dat" INTO TABLE gene_expr_stat;
