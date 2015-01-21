$(document).ready(function() {

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
			var line = JSON.parse(data);
			var plot = $.jqplot('chart', [line], {
				title : 'Température du jour',
				axes : {
					xaxis : {
						renderer : $.jqplot.DateAxisRenderer,
						tickOptions : {
							formatString : '%H'
						},
						tickInterval : '1 hour'
					}
				}
			});
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
