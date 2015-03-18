drop table IF EXISTS rppa_protein_expr;
CREATE TABLE rppa_protein_expr (
	samp_id varchar(63) NOT NULL,
	antibody varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value double NOT NULL,
	primary key (samp_id,antibody),
	index (gene_sym),
	index (antibody),
	index (samp_id),
	index (samp_id,antibody,gene_sym,value)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/RPPA/TCGA_GBM_RPPA.dat" INTO TABLE rppa_protein_expr;
