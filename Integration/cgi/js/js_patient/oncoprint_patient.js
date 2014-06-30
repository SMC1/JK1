var Oncoprint = function(wrapper, params) {
    var that = {};

    var RECT_HEIGHT = 30;
    var TRACK_PADDING = 4;
    var LABEL_PADDING = 45;
    var LITTLE_RECT_HEIGHT = RECT_HEIGHT / 2;
    var MRNA_STROKE_WIDTH = 1;
    var UPREGULATED = "UPREGULATED";
    var DOWNREGULATED = "DOWNREGULATED";
    var MRNA_UP_COLOR = "#FF9999";
    var MRNA_DOWN_COLOR = "#6699CC";
    var mrna_fills = {
        UPREGULATED: "#FF9999",
        DOWNREGULATED: "#6699CC"
    };
    var MUT_COLOR = "rgb(0,215,0)";
	var RPPA_LIGHT = "#D3D3D3";
    var RPPA_DARK = "#000000";
    var cna_fills = {
        none: '#D3D3D3',
        AMPLIFIED: '#FF0000',
        GAINED: '#FFB6C1',
        DIPLOID: '#D3D3D3',
        HEMIZYGOUSLYDELETED: '#8FD8D8',
        HOMODELETED: '#0000FF'
    };

    var data = params.data;
    var query = QueryGeneData(data);
    var genes_list = query.getGeneList();
    var gene_data = data.gene_data;
    var no_genes = gene_data.length;
    var samples_all = query.getSampleList();
	var dbN = data.dbN;
   	var af = data.af;
   	var translate = function(x,y) {
        return "translate(" + x + "," + (y+30) + ")";
    };

    var cleanHugo = function(hugo) {
        // can't have '/' in DOM id
        return hugo.replace("/", "_");
    };

    // global state of the oncoprint
    var state = {
        padding: true,
        width_scalar: 1,
        show_unaltered: true,
        memo_sort: true
    };

    var getVisualizedSamples = function() {
        // get state of samples
        var samples_copy = samples_all.map(function(i) { return i;});

        // todo: note that you must sort first!
        // MemoSort behaves differently when it has different lists, that is,
        // it does not deterministically deal with samples that are equal
        if (state.memo_sort) {
            samples_copy = MemoSort(data, samples_copy, genes_list).sort();
        }

        if (!state.show_unaltered) {
            samples_copy = samples_copy.filter(query.isSampleAltered);
        }

        return samples_copy;
    };

    var getRectWidth = function() {
        var unscaled = 5.5;
        return state.width_scalar * unscaled;
    };

    var getTrianglePath = function(rect_width, up) {

        var getTriangleBase = function() {
            return rect_width / 2;
        };

        var base = getTriangleBase();

        if (up) {
            return "M 0 " + LITTLE_RECT_HEIGHT + " l "  + base + " -" + LITTLE_RECT_HEIGHT
                + " l " + base + " " + LITTLE_RECT_HEIGHT + " l 0 0";
//                return "M 0 7 l 2.75 -7 l 2.75 7 l 0 0";
        }
//        return "M 0 16 l " + base + " 7 l " + base + " -7 l 0 0";
        return "M 0 15 l " + base + " " + LITTLE_RECT_HEIGHT + " l "
            + base + " -" + LITTLE_RECT_HEIGHT + " l 0 0";
//            return "M 0 16 l 2.75 7 l 2.75 -7 l 0 0";
    };

    var getRectPadding = function() {
        var unscaled = 3;
        return state.padding ? (state.width_scalar * unscaled) : 0;
    };

    var getXScale = function(no_samples) {
        return (getRectWidth() + getRectPadding()) * no_samples;
    };

    var getHeight = function() {
        return (RECT_HEIGHT + TRACK_PADDING) * no_genes;
//        return RECT_HEIGHT * no_genes;
        // for some reason, the CSS in the portal creates space between tracks
    };

    // scales
    var x = d3.scale.ordinal().rangeBands([MRNA_STROKE_WIDTH, getXScale(samples_all.length)], 0);

    var y = d3.scale.ordinal().rangeBands([0, getHeight()], 0)
        .domain(genes_list);

    that.getData = function() {
        return params.data;
    };

    var redraw = function(samples_visualized, track, hugo) {
        var join_with_hugo = samples_visualized.map(function(i) {
            return {
                sample: i,
                hugo: hugo
            };
        });

        var sample = track.selectAll('.sample')
            .data(join_with_hugo, function(d) { return d.sample;});

        // enter
        var sample_enter = sample.enter()
            .append('g')
                .attr('class', 'sample')
                .attr('transform', function(d) {
                    return translate(x(d.sample), y(hugo));
                });

        var rect_width = getRectWidth();
		
        var cna = sample_enter.append('rect')
            .attr('class', 'cna')
            .attr('fill', function(d) {
                var cna = query.data(d.sample, hugo, 'cna');
                cna = cna === null ? 'none' : cna;
                return cna_fills[cna];
            })
            .attr('width', rect_width)
            .attr('height', RECT_HEIGHT);

        var mrna = sample_enter.append('rect')
            .attr('class', 'mrna')
            .attr('fill', 'none')
            .attr('stroke-width', MRNA_STROKE_WIDTH)
            .attr('stroke-opacity', 1)
            .attr('width', rect_width)
            .attr('height', RECT_HEIGHT)
            .attr('stroke', function(d) {
                var mrna = query.data(d.sample, hugo, 'mrna');
                if (mrna === UPREGULATED) {
                    return MRNA_UP_COLOR;
                } return MRNA_DOWN_COLOR;
            });

        // remove all the null mrna squares
        mrna.filter(function(d) {
            var mrna = query.data(d.sample, hugo, 'mrna');
            return mrna === null;
        }).remove();
		
		/*** drawing our data here ***/
        var mut = sample_enter.append('rect')
            .attr('class', 'mut')
            .attr('fill', function(d) {
                var mutation = query.data(d.sample, hugo, 'mutation');
				if (hugo.indexOf('RPKM') != -1) {
					mutation++;
					var log_rpkm = (Math.log(mutation)/Math.LN10)/4;
					var gb = 255 - (255*log_rpkm);
					var round_gb = Math.round(gb);
					return "rgb(255," + round_gb + "," + round_gb + ")";
				}else if((hugo.indexOf('CNA') != -1) || (hugo.indexOf('EXPR') != -1) || (hugo.indexOf('xCN') != -1)) {
					var log_value = mutation/4;
					if (mutation >= 0) {
						var gb = 255 - (255*log_value);
						var round_gb = Math.round(gb);
						return "rgb(255," + round_gb + "," + round_gb + ")";
					}else if(mutation < 0) {
						var rg = 255 + (255*log_value);
						var round_rg = Math.round(rg);
						return "rgb(" + round_rg + "," + round_rg + ",255)";
					}
				}else if((hugo.indexOf('PATH') != -1) || (hugo.indexOf('TYPE') != -1)) {
					var log_value = mutation;
					if (mutation >= 0) {
						var gb = 255 - (255*log_value);
						var round_gb = Math.round(gb);
						return "rgb(255," + round_gb + "," + round_gb + ")";
					}else if(mutation < 0) {
						var rg = 255 + (255*log_value);
						var round_rg = Math.round(rg);
						return "rgb(" + round_rg + "," + round_rg + ",255)";
					}
				}
				else {
                	var freq = query.data(d.sample, hugo, 'freq');
                	if (freq >0) {
                    	var rb = 255 - (255*freq);
                    	var round_rb = Math.round(rb);
                    	return "rgb(" + round_rb + ",255," + round_rb+ ")";
                	}else if (mutation === hugo) {
                    	return "#d3d3d3";
                	}return MUT_COLOR;
				}
            })
			.attr('stroke', '#000000')
			.attr('stroke-width', function(d) {
				var mutation = query.data(d.sample, hugo, 'mutation');
				if (mutation === null){
					return 0;
				}return 0.7;
			})
            .attr('y', 0)
            .attr('width', rect_width)
            .attr('height', LITTLE_RECT_HEIGHT);

        // remove all the null mutation squares
        mut.filter(function(d) {
            var mutation = query.data(d.sample, hugo, 'mutation');
            return mutation === null;
        }).remove();

		/*** draw pair data here ***/
		var mut2 = sample_enter.append('rect')
			.attr('class', 'mut2')
            .attr('fill', function(d) {
				if (hugo.indexOf('RPKM') != -1) {
					var pair = query.data(d.sample, hugo, 'pair');
					var pair_rpkm = pair.split(":")[1];
					if (pair_rpkm === "null"){
						return "#d3d3d3";
					}
					else {
						pair_rpkm++;
						var log_rpkm = (Math.log(pair_rpkm)/Math.LN10)/4;
						var gb = 255 - (255*log_rpkm);
						var round_gb = Math.round(gb);
						return "rgb(255," + round_gb + "," + round_gb + ")";	
					}
				}else if ((hugo.indexOf('CNA') != -1) || (hugo.indexOf('EXPR') != -1) || (hugo.indexOf('xCN') != -1)) {
					var pair = query.data(d.sample, hugo, 'pair');
					var pair_value = pair.split(":")[1];
					if (pair_value === "null") {
						return "#d3d3d3";
					}
					else {
						var log_value = pair_value/4;
						if (log_value >= 0) {
							var gb = 255 - (255*log_value);
							var round_gb = Math.round(gb);
							return "rgb(255," + round_gb + "," + round_gb + ")";
						}else if(log_value < 0) {
							var rg = 255 + (255*log_value);
							var round_rg = Math.round(rg);
							return "rgb(" + round_rg + "," + round_rg + ",255)";
						}
					}
				}else if ((hugo.indexOf('PATH') != -1) || (hugo.indexOf('TYPE') != -1)) {
					var pair = query.data(d.sample, hugo, 'pair');
					var pair_value = pair.split(":")[1];
					if (pair_value === "null") {
						return "#d3d3d3";
					}
					else {
						var log_value = pair_value;
						if (log_value >= 0) {
							var gb = 255 - (255*log_value);
							var round_gb = Math.round(gb);
							return "rgb(255," + round_gb + "," + round_gb + ")";
						}else if(log_value < 0) {
							var rg = 255 + (255*log_value);
							var round_rg = Math.round(rg);
							return "rgb(" + round_rg + "," + round_rg + ",255)";
						}
					}
				}
				else {
                	var pair = query.data(d.sample, hugo, 'pair');
					var pair_freq = pair.split(":")[1];
                	if(pair_freq > 0) {
                    	var rb = 255 - (255*pair_freq);
                    	var round_rb = Math.round(rb);
                    	return "rgb(" + round_rb + ",255," + round_rb+ ")";
                	}else if (pair_freq === "0") {
                   		return "#d3d3d3";
                	}else if (pair_freq === "null") {
                    	return "#d3d3d3";
                	}return MUT_COLOR;
				}
            })
			.attr('stroke', '#000000')
			.attr('stroke-width', function(d) {
				var pair = query.data(d.sample, hugo, 'pair');
				var pair_id = pair.split(":")[0];
				var pair_freq = pair.split(":")[1];
				if (pair_freq === "null"){
					return 0;
				}return 0.7;
			})
			.attr('y', LITTLE_RECT_HEIGHT)
			.attr('width', rect_width)
			.attr('height', LITTLE_RECT_HEIGHT);		

		mut2.filter(function(d) {
			var pair = query.data(d.sample, hugo, 'pair');
			return pair === null;
		}).remove();
		/*******************************************************************************************************/

        var up_triangle = getTrianglePath(rect_width, true);
        var down_triangle = getTrianglePath(rect_width, false);

        var rppa = sample_enter.append('path')
            .attr('class', 'rppa')
            .attr('fill', function(d) {
                if (query.data(d.sample, hugo, 'cna') === null) {
                    return RPPA_DARK;
                }
                return RPPA_LIGHT;
            })
            .attr('d', function(d) {
                var rppa = query.data(d.sample, hugo, 'rppa');

                if (rppa === UPREGULATED) {
                    return up_triangle;
                }
                if (rppa === DOWNREGULATED) {
                    return down_triangle;
                }
                if (rppa === null) {
                    return 'M 0 0';
                }
            });

        rppa.filter(function(d) {
            var rppa = query.data(d.sample, hugo, 'rppa');

            return rppa === null;
        }).remove();

        // exit
        var sample_exit = sample.exit().remove();
    };

    var svg;        // global scope
    that.getSvg = function() { return svg; };

    // oncoprint legend
    //
    var legend = function(data_types) {

        var captions = {
            cna: {
                AMPLIFIED: "Amplification",
                GAINED: "Gain",
                DIPLOID: "Diploid",
                HEMIZYGOUSLYDELETED: "Hemizygous Deletion",
                HOMODELETED: "Homozygous Deletion"
            },
            mrna: {
                UPREGULATED: "mRNA Upregulation",
                DOWNREGULATED: "mRNA Downregulation"
            },
            rppa: {
                UPREGULATED: "RPPA Upregulation",
                DOWNREGULATED: "RPPA Downregulation"
            },
            mutation: "Mutation"
        };


        var text_padding = 15;

        var legend_el = d3.select('#oncoprint_legend');
        legend_el.style('margin-left', getRectWidth() + label_width + 2 + "px");

        var getSvg = function(label_str) {
            var svg = legend_el.append('svg');

            var el_width = function(label_str) {
                var l = label_str.split("");
                var scalar = 7;
                var affine = 25;
                return affine + scalar * l.length;
            };

            svg.attr('height', RECT_HEIGHT);
            svg.attr('width', el_width(label_str));
            return svg;
        };

        var range = query.getDataRange();

        var rect_width = getRectWidth();

        var cna_order = {AMPLIFIED:4, HOMODELETED:3, GAINED:2, HEMIZYGOUSLYDELETED:1, DIPLOID: 0, null:0};
        var cnas = _.keys(range.cna);
        cnas = cnas.sort(function(a,b) {
            return cna_order[b] - cna_order[a];
        });

        cnas.forEach(function(cna) {
            var svg = getSvg(captions.cna[cna]);

            svg.append('rect')
                .attr('fill', function(d) {
                    return cna_fills[cna];
                })
                .attr('width', rect_width)
                .attr('height', RECT_HEIGHT);

            var text = svg.append('text')
                .attr('fill', 'black')
                .attr('x', text_padding)
                .attr('y', .75 * RECT_HEIGHT)
                .text(captions.cna[cna]);
        });

        for (var mrna in range.mrna) {
            var svg = getSvg(captions.mrna[mrna]);

            svg.append('rect')
                .attr('fill', cna_fills['none'])
                .attr('stroke-width', MRNA_STROKE_WIDTH)
                .attr('stroke-opacity', 1)
                .attr('width', rect_width)
                .attr('height', RECT_HEIGHT)
                .attr('stroke', mrna_fills[mrna]);

            var text = svg.append('text')
                .attr('fill', 'black')
                .attr('x', text_padding)
                .attr('y', .75 * RECT_HEIGHT)
                .text(captions.mrna[mrna]);
        }

        if (!$.isEmptyObject(range.mutations)) {
            var svg = getSvg(captions.mutation);

            // background of none
            svg.append('rect')
                .attr('fill', cna_fills['none'])
                .attr('width', rect_width)
                .attr('height', RECT_HEIGHT);

            // little mutation square
            svg.append('rect')
                .attr('fill', MUT_COLOR)
                .attr('y', LITTLE_RECT_HEIGHT)
                .attr('width', rect_width)
                .attr('height', LITTLE_RECT_HEIGHT);

            var text = svg.append('text')
                .attr('fill', 'black')
                .attr('x', text_padding)
                .attr('y', .75 * RECT_HEIGHT)
                .text(captions.mutation);
        }

        for (var rppa in range.rppa) {
            var svg = getSvg(captions.rppa[rppa]);

            var up_triangle = getTrianglePath(rect_width, true);
            var down_triangle = getTrianglePath(rect_width, false);

            // background of none
            svg.append('rect')
                .attr('fill', cna_fills['none'])
                .attr('width', rect_width)
                .attr('height', RECT_HEIGHT);

            svg.append('path')
                .attr('fill', 'black')
                .attr('d', function(d) {
                    if (rppa === UPREGULATED) {
                        return up_triangle;
                    }
                    if (rppa === DOWNREGULATED) {
                        return down_triangle;
                    }
                    if (rppa === null) {
                        return 'M 0 0';
                    }
                });

            var text = svg.append('text')
                .attr('fill', 'black')
                .attr('x', text_padding)
                .attr('y', .75 * RECT_HEIGHT)
                .text(captions.rppa[rppa]);
        }

        legend_el.append('p')
            .style('font-size', '12px')
            .style('margin-bottom', 0)
            .style('margin-top', 7 + 'px')
            .text('Copy number alterations are putative.');
    };
    //
    // end oncoprint legend

	/*** generate qtip ***/
    var makeQtip = function() {
        var formatMutation = function(sample, hugo) {
            // helper function
            var mutation = query.data(sample, hugo, 'mutation');
            var pair = query.data(sample, hugo, 'pair');
			var pair_id = pair.split(":")[0];
			var pair_freq = pair.split(":")[1];
			var freq = '';
			var fraction_p = '';
			var fraction_r = '';

			if ((hugo.indexOf('RPKM') != -1) || (hugo.indexOf('CNA') != -1) || (hugo.indexOf('EXPR') != -1) || (hugo.indexOf('PATH') != -1) || (hugo.indexOf('TYPE') != -1) || (hugo.indexOf('xCN') != -1)) {
				if (mutation === null) {
					freq ='';
				}else {
					freq = String(mutation).substr(0, mutation.indexOf('.')+3);
				}
				
				if ((pair_freq !== null) && (pair_freq !== 'null')){
					pair_freq = pair_freq.substr(0, pair_freq.indexOf('.')+3);
				}
			}
			else {
            	freq = query.data(sample, hugo, 'freq');
            	var fraction_w = query.data(sample, hugo, 'fraction');
            	if (freq > 0) {
                	var tmp_freq = String(freq);
                	var tmp = tmp_freq.substr(0,4);
                	freq = tmp;
    	            fraction_p += " (" + fraction_w.substr(0, fraction_w.indexOf(":")) + ")";
        	    }
            	if (pair_freq > 0) {
                	var tmp_freq = pair_freq.substr(0,4);
                	pair_freq = tmp_freq;
                	fraction_r += " (" + fraction_w.substr(fraction_w.indexOf(":")+1) + ")";
            	}

			}

			if ((freq === 'null') || (freq === 'nofreq')) {
				freq = '';
			}else {
				if((freq == 0) || (freq == '0')) {
					freq = ', ' + freq + ' (af>' + af + ')';
				}else {
					freq = ', ' + freq;
				}
			}

			if ((pair_freq === 'null') || (pair_freq === 'nofreq') || (pair_freq ===null)) {
				pair_freq = '';
			}else {
				if((pair_freq == 0) || (pair_freq == '0')) {
					pair_freq = ', ' + pair_freq + ' (af>' + af + ')';
				}else {
					pair_freq = ', ' + pair_freq;
				}
			}

            if (mutation !== null) {
               	return "<b>" + hugo + "</b><br> P: " + patientViewUrl(sample) + freq + fraction_p + "<br> R: " + patientViewUrl(pair_id) + pair_freq + fraction_r + "<br>";
           	}else if(pair !== null) {
               	return "<b>" + hugo + "</b><br> P: " + patientViewUrl(sample) + "<br> R: " + patientViewUrl(pair_id) + pair_freq + fraction_r + "<br>";
           	}return "";
        };

        var patientViewUrl = function(sample_id) {
            // helper function
            var href = "http://119.5.134.58/cgi-bin/ircr_samp.py?dbN="+dbN+"&sId="+sample_id;

            return "<a href='" + href + "'>" + sample_id + "</a>";
        };


        // make qtip
        d3.selectAll('.sample').each(function(d, i) {
            $(this).qtip({
                content: 'oncoprint qtip failed',
                //show : 'mouseover',
                events: {
                    render: function(event, api) {
                        var content = '<font size="2">' + formatMutation(d.sample, d.hugo) + '</font>';
                        api.set('content.text', content);
                    }
                },
                hide: { fixed: true, delay: 100 },
                style: { classes: 'ui-tooltip-light ui-tooltip-rounded ui-tooltip-shadow ui-tooltip-lightyellow' },
                position: {my:'left top',at:'bottom center'}
            });
        });
    };
	/*******************************************************************************************************************************/

	/*** set scale bar ***/
    var widthScrollerSetup = function() {
        $('<div>', { id: "width_slider", width: "200"})
            .slider({
                text: "Adjust Width ",
                min: .1,
                max: 6,
                step: .02,
                value: 1,
                change: function(event, ui) {
                    console.log(ui.value);
                    oncoprint.scaleWidth(ui.value);
					
					var firsttrack = d3.select('.track');
					firsttrack.selectAll('text').remove();
					var firsttext = d3.select('#label');
					firsttext.selectAll('#pair').remove();
                    var alltrack = d3.selectAll('.track');
                    alltrack.selectAll('#freq').remove();

					if(ui.value > 4) {
						var firsttext = d3.select('#label');
						var plabel = firsttext.insert('text')
							.attr('id', 'pair')
							.attr('text-anchor', 'end')
							.attr('x', +100)
							.attr('y', +10)
							.attr('font-size', 13)
							.text('P : ');
						var rlabel = firsttext.insert('text')
							.attr('id', 'pair')
							.attr('text-anchor', 'end')
							.attr('x', +100)
							.attr('y', +25)
							.attr('font-size', 13)
							.text('R : ');

						var firsthugo = genes_list[0];
						var samp_index = firsttrack.selectAll('.sample').insert('text')
							.attr('text-anchor', 'start')
							.attr('y', -20)
							.attr('font-size', 13)
							.text(function(d) { 
								return  d.sample;
							});
						var samp_index2 = firsttrack.selectAll('.sample').insert('text')
							.attr('text-anchor', 'start')
							.attr('y', -5) 
							.attr('font-size', 13)
							.text(function(d) {
								var pair = query.data(d.sample, firsthugo, 'pair');
								var pair_id = pair.split(":")[0];
								return  pair_id;
							});

                        if(ui.value === 6) {
                            var alltrack = d3.selectAll('.track');
                            var allsample = alltrack.selectAll('.sample').insert('text')
                                .attr('id', 'freq')
                                .attr('text-anchor', 'start')
                                .attr('x', +5)
                                .attr('y', +12)
                                .attr('font-size', 10)
                                .text( function(d) {
									if (d.hugo.indexOf('RPKM') != -1) {
										var rpkm = query.data(d.sample, d.hugo, 'mutation');
										if (rpkm == null) {
											return null;
										}else {
											var sub_rpkm = String(rpkm).substr(0, rpkm.indexOf('.'));
											return sub_rpkm;
										}
									}else if((d.hugo.indexOf('CNA') != -1) || (d.hugo.indexOf('EXPR') != -1) || (d.hugo.indexOf('PATH') != -1) || (d.hugo.indexOf('TYPE') != -1) || (d.hugo.indexOf('xCN') != -1)) {
										var value_a = query.data(d.sample, d.hugo, 'mutation');
										if(value_a == null) {
											return null;
										}else {
											var sub_value = String(value_a).substr(0, value_a.indexOf('.')+3);
											return sub_value;
										}
									}else {
                                    	var freq = query.data(d.sample, d.hugo, 'freq');
                                    	var sub_freq = String(freq).substr(0,4);
                                    	if(freq > 0) {
                                        	return sub_freq;
                                    	}return null;
									}
                                });

                            var allpair = alltrack.selectAll('.sample').insert('text')
                                .attr('id', 'freq')
                                .attr('text-anchor', 'start')
                                .attr('x', +5)
                                .attr('y', +26)
                                .attr('font-size', 10)
                                .text( function(d) {
                                    var pair = query.data(d.sample, d.hugo, 'pair');
									var pair_freq = pair.split(":")[1];
									if (d.hugo.indexOf('RPKM') != -1){
										var pair_rpkm = String(pair_freq).substr(0, pair_freq.indexOf('.'));
										return pair_rpkm;
									}else if((d.hugo.indexOf('CNA') != -1) || (d.hugo.indexOf('EXPR') != -1) || (d.hugo.indexOf('PATH') != -1) || (d.hugo.indexOf('TYPE') != -1) || (d.hugo.indexOf('xCN') != -1)) {
										if (pair_freq !== 'null') {
											var pair_value = String(pair_freq).substr(0, pair_freq.indexOf('.')+3);
											return pair_value;
										}
									}else {
                                    	var sub_pair_freq = String(pair_freq).substr(0,4);
                                    	if(pair_freq > 0) {
                                        	return sub_pair_freq;
                                    	}return null;
									}
                                });
                        }
					}
				}
            }).appendTo($('#oncoprint_controls #zoom'));
    };
	/*************************************************************************************************************************/

    that.draw = function() {

        label_width = (function() {
            // calculate the length of the longest label,
            // save it in the global variable for later use

            var label_svg = d3.select('body').append('svg');
            // put in a temporary svg for the sake of calculating text width

            gene_data.forEach(function(gene_obj) {
                var label = label_svg.append('text');
                var cleaned_hugo = cleanHugo(gene_obj.hugo);

                label.append('tspan')
                    .text(cleaned_hugo);
            });

            var longest = d3.max(
                label_svg.selectAll('text')[0]
                    .map(function(text, i) {return text.getBBox().width; })
            );

            label_svg.remove();
            // bye bye pretend svg

            return LABEL_PADDING + longest + 20;

        })();

        var $header = $('<div>', {id:'oncoprint_header'});
        $(wrapper).append($header);

        $header.append(
            '<!--p>Case Set: ' + params.case_set_str + '</p--></div>'
                + '<p>Altered in ' + query.altered_samples.length + ' (' + d3.format("%")(query.percent_altered) + ') of '
                + query.getSampleList().length + ' cases </p></div>');

        var visualized_samples = getVisualizedSamples();

        x.domain(visualized_samples);

//        var table_wrap = d3.select(wrapper).insert('table', ':first-child').append('tr');
        var table_wrap = d3.select(wrapper).append('table').append('tr');

        var label_svg = table_wrap.insert('td').insert('svg', ':first-child')
            .attr('id', "label")
            .attr('width', label_width+30)
            .attr('height', getHeight()+30);

        // td-content is some parent td
        var body_wrap = table_wrap.append('td').append('div')
            .style('width', $('#td-content').width() - 70 - label_width + 'px') // buffer of, say, 70
            .style('display', 'inline-block')
            .style('overflow-x', 'auto')
            .style('overflow-y', 'auto');

        svg = body_wrap.append('svg')
            .attr('id', 'body')
            .attr('width', getXScale(samples_all.length))
            .attr('height', getHeight() + 30);	
		
        gene_data.forEach(function(gene_obj) {

            var hugo = gene_obj.hugo;
            var cleaned_hugo = cleanHugo(hugo);
			
            var track = svg.append('g')
                .attr('class', 'track');

            var label = label_svg.append('text')
                .attr('x', 0)
                .attr('y', y(hugo) + .75 * RECT_HEIGHT+30);

            label.append('tspan')
                .attr('font-weight', 'bold')
                .attr('text-anchor', 'start')
                .text(cleaned_hugo);

            label.append('tspan')
                .attr('text-anchor', 'start')
                .attr('x', label_width-40)
                .text(gene_obj.percent_altered);

            redraw(visualized_samples, track, hugo);
        });
		
        makeQtip();

        if (params.vis_key) {       // toggle the key to the visualization
            legend();
        }

        if (params.customize) {         // toggle the setup of the customization controls
            widthScrollerSetup();
        }
    };

    var transition = function() {
        // helper function

        var samples_visualized = getVisualizedSamples();
        var no_samples = samples_visualized.length;

        x.domain(samples_visualized);
        x.rangeBands([MRNA_STROKE_WIDTH, getXScale(no_samples)]);

        svg.selectAll('.track')[0].forEach(function(val, i) {

            var hugo = genes_list[i];

//            var transition = d3.select(val).transition();
            var transition = d3.select(val);

            transition.selectAll('.sample')
//                .transition()
//                .duration(1000)
                .attr('transform', function(d) {
                    return translate(x(d.sample), y(hugo));
                });

            var rect_width = getRectWidth();
            transition.selectAll('rect')
//                .transition()
//                .duration(1000)
                .attr('width', rect_width)

            var up_triangle = getTrianglePath(rect_width, true);
            var down_triangle = getTrianglePath(rect_width, false);
            transition.selectAll('.rppa')
//                .transition()
//                .duration(1000)
                .attr('d', function(d) {
                    var rppa = query.data(d.sample, hugo, 'rppa');

                    if (rppa === UPREGULATED) {
                        return up_triangle;
                    }
                    if (rppa === DOWNREGULATED) {
                        return down_triangle;
                    }
                });
        });

        svg.transition().duration(1000).style('width', getXScale(no_samples));
    };

    that.memoSort = function() {

        if (state.memo_sort) {
            return;
        }

        state.memo_sort = true;

        transition();
    };

    that.defaultSort = function() {

        if (!state.memo_sort) {
            return;
        }

        state.memo_sort = false;

        transition();
    };

    that.toggleWhiteSpace = function() {
        state.padding = !state.padding;

        transition();
    };

    that.scaleWidth = function(scalar) {
        state.width_scalar = scalar;
        transition();
    };

    that.toggleUnaltered = function() {
        state.show_unaltered = !state.show_unaltered;

        var samples_visualized = getVisualizedSamples();

        gene_data.forEach(function(gene, i) {
            var track = d3.select(d3.select(wrapper).selectAll('.track')[0][i]);
            redraw(samples_visualized, track, gene.hugo);
            transition();
        });

        makeQtip();
    };

//  For the given oncoprint reference, returns the SVG Dom as string
//  for the body canvas.
    that.getOncoPrintBodyXML = function() {
        // hard coding this for now

        var labels = $('#oncoprint svg#label').children().clone();
        var tracks = $('#oncoprint svg#body').children().clone();

        tracks.each(function(track_i, track) {
            // for each track loop over the samples
            $(track).children().each(function(sample_i, sample) {
                $(sample).attr('transform', translate(x(sample_i) + label_width, y(track_i)));
            });
        });

        var number_of_samples = $(tracks[0]).children().length;

        var export_svg = $('<svg>')
            .attr('width', getXScale(number_of_samples) + label_width +100)
            .attr('height', getHeight() +100);

        export_svg
            .append(labels)
            .append(tracks);
//            .append(visualizedKeys(query.data_types));

        return (new XMLSerializer()).serializeToString(export_svg[0]);
    };

    return that;
};

