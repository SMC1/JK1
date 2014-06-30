drop table IF EXISTS methyl_rpkm;
CREATE TABLE methyl_rpkm (
	geneName varchar(31),
	platform varchar(31),
	loc varchar(31),
	nSamp smallint unsigned,
	r float,
	index (geneName)
);

LOAD DATA LOCAL INFILE "/home/heejin/JK1/Integration/wg_methyl_pos_rpkm_log.txt" INTO TABLE methyl_rpkm;
