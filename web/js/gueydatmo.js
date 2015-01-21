$(document).ready(function() {

	// Vars
	var plotOpt = {
		title : 'Température du jour',
		axes : {
			xaxis : {
				renderer : $.jqplot.DateAxisRenderer,
				tickOptions : {
					formatString : '%R'
				}
			}
		},
		highlighter : {
			show : true,
			sizeAdjust : 7.5
		},
		cursor : {
			show : false
		}
	};
	var plot = $.jqplot('chart', [[20]], plotOpt);

	// Buttons callbacks
	$("#devicelist-btn").click(function(e) {
		$.get("/devicelist", function(data) {
			$("#devicelist-raw").html(data);
			$("#devicelist-raw").show();
		});
		e.preventDefault();
	});
	$("#getuser-btn").click(function(e) {
		$.get("/getuser", function(data) {
			$("#getuser-raw").html(data);
			$("#getuser-raw").show();
		});
		e.preventDefault();
	});
	$("#getmeasure-btn").click(function(e) {
		$.get("/getmeasure", function(data) {
			$("#chart").html("");
			var line = JSON.parse(data);
			plot.destroy();
			plot = $.jqplot('chart', [line], plotOpt);
		});
		e.preventDefault();
	});
	$("#getthermstate-btn").click(function(e) {
		$.get("/getthermstate", function(data) {
			$("#getthermstate-raw").html(data);
			$("#getthermstate-raw").show();
		});
		e.preventDefault();
	});

});
