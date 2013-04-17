drop table IF EXISTS census;
CREATE TABLE census (
	gene_sym varchar(31),
	gene_desc text,
	chrom varchar(31) NOT NULL,
	somatic char(1) NOT NULL,
	germline char(1) NOT NULL,
	tumor_soma text,
	tumor_germ text,
	syndrome text,
	mut_type varchar(31),
	tloc_partner text,
	primary key (gene_sym)
);

LOAD DATA LOCAL INFILE "/data1/Sequence/geneinfo/census.dat" INTO TABLE census;
