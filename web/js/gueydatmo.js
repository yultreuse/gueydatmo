$(document).ready(function() {
	$("#devicelist-btn").click(function(e) {
		$.get("/devicelist",function(data){
			$("#devicelist-raw").html(data);
			$("#devicelist-raw").show();
		});
		e.preventDefault();
	});
	$("#getuser-btn").click(function(e) {
		$.get("/getuser",function(data){
			$("#getuser-raw").html(data);
			$("#getuser-raw").show();
		});
		e.preventDefault();
	});
	$("#getmeasure-btn").click(function(e) {
		$.get("/getmeasure",function(data){
			$("#getmeasure-raw").html(data);
			$("#getmeasure-raw").show();
		});
		e.preventDefault();
	});
	$("#getthermstate-btn").click(function(e) {
		$.get("/getthermstate",function(data){
			$("#getthermstate-raw").html(data);
			$("#getthermstate-raw").show();
		});
		e.preventDefault();
	});
}); 