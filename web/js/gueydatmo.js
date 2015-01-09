$(document).ready(function() {
	$("#devicelist-btn").click(function(e) {
		$.get("/devicelist",function(data){
			$("#devicelist-raw").html(data);
			$("#devicelist-raw").show();
		});
		e.preventDefault();
	});
}); 