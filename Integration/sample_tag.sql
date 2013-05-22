drop table IF EXISTS sample_tag;

CREATE TABLE sample_tag (
	samp_id varchar(63) NOT NULL,
	tag varchar(63) NOT NULL,
	primary key (samp_id,tag)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/clinical/sample_tag.dat" INTO TABLE sample_tag;
/* LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/clinical/sample_tag.dat" INTO TABLE sample_tag; */
