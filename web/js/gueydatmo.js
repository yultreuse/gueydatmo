$(document).ready(function() {
	
	// Get context with jQuery - using jQuery's .get() method.
	var ctx = $("#myChart").get(0).getContext("2d");
	var data = {
		labels : ["January", "February", "March", "April", "May", "June", "July"],
		datasets : [{
			label : "My First dataset",
			fillColor : "rgba(220,220,220,0.2)",
			strokeColor : "rgba(220,220,220,1)",
			pointColor : "rgba(220,220,220,1)",
			pointStrokeColor : "#fff",
			pointHighlightFill : "#fff",
			pointHighlightStroke : "rgba(220,220,220,1)",
			data : [65, 59.6, 80, 81, 56, 55, 40]
		}]
	};
	var options = {};
	var myLineChart = new Chart(ctx).Line(data, options);
	
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
			$("#getmeasure-raw").html(data);
			$("#getmeasure-raw").show();
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
