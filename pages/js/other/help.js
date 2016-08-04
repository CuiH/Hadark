var oldonload = window.onload;
window.onload = function() {
	oldonload();
	$("#goback").click(function() {
		//window.location.href = "http://" + CURRENT_URL_2 + "/homepage";
		history.back(-1);
	});
	$("#feature").click(function() {
		window.location.href = "http://" + CURRENT_URL_2 + "/feature.html";
	});
	var height = window.innerHeight - $("#main").offset().top;
	var height2 = $("#top").height();
    $("#main").css("min-height", height + "px");
    $("#toc").offset({top:height2});
    var left1 =  $("#toc").offset().left + $("#toc").width();
    $("#mainContent").offset({left:left1});
    $("#main").css("max-height", "");
    if (window.innerHeight < (850 + height2) ) {
    	$("#toc").css("font-size", "1.2rem");
    }
    if (window.innerHeight < (602 + height2) ) {
    	$("#toc").css("font-size", "1rem");
    }
}