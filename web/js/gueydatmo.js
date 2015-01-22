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
	$("#getmeasure-btn").click(function(e) {
		$.get("/getmeasure", function(data) {
			$("#chart").html("");
			var line = JSON.parse(data);
			plot.destroy();
			plot = $.jqplot('chart', [line], plotOpt);
			$("#debug-screen").html("measure updated");
		});
	});
	
	function debugCallback(data) {
		$("#debug-screen").html(data);
	}
	
	$("#getuser-btn").click(function(e) {
		$.get("/getuser", debugCallback);
	});
	
	$("#devicelist-btn").click(function(e) {
		$.get("/devicelist", debugCallback);
	});
	
	$("#getthermstate-btn").click(function(e) {
		$.get("/getthermstate", debugCallback);
	});

});
