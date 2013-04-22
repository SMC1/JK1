var oncoPrintParams = {
    cancer_study_id: "brca_tcga",
    case_set_str: "SMC",
    num_cases_affected: "333",
    percent_cases_affected: "69%",
    vis_key: true,
    //customize: true
   //vis_key: false,
    customize: true
};

$.get('/js/gene_data.json', function(data) {

    oncoPrintParams['data'] = data;
    oncoprint = Oncoprint($('#oncoprint')[0], oncoPrintParams);

    oncoprint.draw();
});
