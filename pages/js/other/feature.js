var oldonload = window.onload;
window.onload = function() {
	oldonload();
	$("#goback").click(function() {
		//window.location.href = "http://" + CURRENT_URL_2 + "/homepage";
		history.back(-1);
	});
	$("#help").click(function() {
		window.location.href = "http://" + CURRENT_URL_2 + "/help.html";
	});
	var height = window.innerHeight - $("#main").offset().top;
    $("#main").css("min-height", height + "px");
}