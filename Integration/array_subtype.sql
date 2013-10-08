drop table IF EXISTS array_subtype;
CREATE TABLE array_subtype (
	samp_id char(12),
	P float,
	N float,
	C float,
	M float,
	U float,
	subtype char(1),
	primary key (samp_id)
);

LOAD DATA LOCAL INFILE "/EQL1/Phillips/Phillips_U133A_TCGA_subtype.dat" INTO TABLE array_subtype;
