var oldonload = window.onload;
window.onload = function() {
	oldonload();
	$("#goback").click(function() {
		window.location.href = "http://" + CURRENT_URL_2 + "/homepage";
	});
}