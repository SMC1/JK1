create temporary table id as \
	select distinct samp_id from array_gene_expr UNION \
	select distinct samp_id from array_pathway UNION \
	select distinct samp_id from array_subtype UNION \
	select pId samp_id from clinical;

create temporary table nrp1 select samp_id, z_score nrp1 from array_gene_expr where gene_sym='NRP1';

create temporary table sema3a select samp_id, z_score sema3a from array_gene_expr where gene_sym='SEMA3A';

create temporary table tgfb select samp_id, activity tgfb from array_pathway where pathway='TGFb';

create temporary table subtype select samp_id, subtype from array_subtype;

create temporary table survival select pId samp_id, age, gender, days_death, days_followup from clinical;

SELECT samp_id pId, age, gender, days_death, days_followup, nrp1, sema3a, tgfb, subtype FROM id \
	left join nrp1 using (samp_id) \
	left join sema3a using (samp_id) \
	left join tgfb using (samp_id) \
	left join subtype using (samp_id) \
	left join survival using (samp_id);
