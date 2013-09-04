drop table IF EXISTS subtype;
CREATE TABLE subtype (
	samp_id char(12),
	P float,
	N float,
	C float,
	M float,
	U float,
	subtype char(1),
	primary key (samp_id)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_subtype.dat" INTO TABLE subtype;
