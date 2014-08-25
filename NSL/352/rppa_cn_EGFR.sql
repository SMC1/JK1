create temporary table t_cn 
select samp_id,value_log2 cn_log2 from array_cn where gene_sym='EGFR' and samp_id like 'TCGA%' order by samp_id;

create temporary table t_prot 
select samp_id,value prot from rppa_protein_expr where antibody='EGFR-R-C' and samp_id like 'TCGA%' order by samp_id;

create temporary table t_Y1068 
select samp_id,value Y1068 from rppa_protein_expr where antibody like 'EGFR_pY1068%' and samp_id like 'TCGA%' order by samp_id;

create temporary table t_Y1173 
select samp_id,value Y1173 from rppa_protein_expr where antibody like 'EGFR_pY1173%' and samp_id like 'TCGA%' order by samp_id;

create temporary table t_Y992 
select samp_id,value Y992 from rppa_protein_expr where antibody like 'EGFR_pY992%' and samp_id like 'TCGA%' order by samp_id;

create temporary table t_clin 
select pId samp_id,days_death,days_followup from clinical order by samp_id;

create temporary table t 
select * from t_cn join t_prot using (samp_id) join t_Y1068 using (samp_id) join t_Y1173 using (samp_id) join t_Y992 using (samp_id) join t_clin using (samp_id) order by samp_id;

select * from t order by cn_log2;
