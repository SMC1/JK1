drop table IF EXISTS splice_normal;
CREATE TABLE splice_normal (
	samp_id char(12) NOT NULL,
	loc1 varchar(31) NOT NULL, -- hg19
	loc2 varchar(31) NOT NULL,
	nReads mediumint unsigned NOT NULL,
	nPos tinyint unsigned NOT NULL,
	primary key (samp_id,loc1,loc2),
	index (samp_id,loc1),
	index (samp_id,loc2),
	index (samp_id)
);

ALTER TABLE splice_normal DISABLE KEYS;
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_normal_NSL36.dat" INTO TABLE splice_normal; */
/* LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_normal_170.dat" IGNORE INTO TABLE splice_normal; */
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip_normal/splice_normal_NSL45.dat" INTO TABLE splice_normal;
/*LOAD DATA LOCAL INFILE "/EQL2/SGI_20131031/RNASeq/results/exonSkip_normal/splice_normal_30.dat" INTO TABLE splice_normal;*/
/** batch load and reprocess all**/
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip_normal/splice_normal_SGI20131031_30.dat" INTO TABLE splice_normal;
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip_normal/splice_normal_SGI20131119_6.dat" INTO TABLE splice_normal;
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip_normal/splice_normal_SGI20131212_6.dat" INTO TABLE splice_normal;
ALTER TABLE splice_normal ENABLE KEYS;
drop table if exists splice_normal_loc1;
create table splice_normal_loc1 as select samp_id,loc1,sum(nReads) nReads_w1 from splice_normal group by samp_id,loc1;
alter table splice_normal_loc1 add index (samp_id,loc1);

drop table if exists splice_normal_loc2;
create table splice_normal_loc2 as select samp_id,loc2,sum(nReads) nReads_w2 from splice_normal group by samp_id,loc2;
alter table splice_normal_loc2 add index (samp_id,loc2);

/** load and process only new samples **/
/*CREATE TEMPORARY TABLE splice_normal_tmp LIKE splice_normal;
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip_normal/splice_normal_SGI20131212_6.dat" INTO TABLE splice_normal_tmp;
ALTER TABLE splice_normal_tmp ADD INDEX (samp_id,loc1);
ALTER TABLE splice_normal_tmp ADD INDEX (samp_id,loc2);
ALTER TABLE splice_normal_tmp ADD INDEX (samp_id);
ALTER TABLE splice_normal DISABLE KEYS;
INSERT INTO splice_normal SELECT * from splice_normal_tmp;
ALTER TABLE splice_normal ENABLE KEYS;

ALTER TABLE splice_normal_loc1 DISABLE KEYS;
INSERT INTO splice_normal_loc1 SELECT samp_id,loc1,sum(nReads) nReads_w1 FROM splice_normal_tmp GROUP BY samp_id,loc1;
ALTER TABLE splice_normal_loc1 ENABLE KEYS;
ALTER TABLE splice_normal_loc2 DISABLE KEYS;
INSERT INTO splice_normal_loc2 SELECT samp_id,loc2,sum(nReads) nReads_w2 FROM splice_normal_tmp GROUP BY samp_id,loc2;
ALTER TABLE splice_normal_loc2 ENABLE KEYS;*/
