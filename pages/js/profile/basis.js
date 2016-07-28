var profile = angular.module("profileApp", [])

var CURRENT_URL = "172.18.231.84"

var AUTH = "hwb:hwb"

// get file name from input_file
function getFileName(filePath) {
	var p1 = filePath.lastIndexOf('/')
	var p2 = filePath.lastIndexOf('\\')
	var pos = Math.max(p1, p2)
	return filePath.substring(pos+1)
}

// show percentage of upload
function onprogress(evt){
	var loaded = evt.loaded;		 //已经上传大小情况 
	var tot = evt.total;			//附件总大小 
	var per = Math.floor(100*loaded/tot);	//已经上传的百分比 
	$('#progress_modal_bar').progress({
		percent: per
	});

	if (per >= 100) {
		$("#progress_modal_bar_message").text("Server is doing something, please wait")
	}
}

// init the result modal
function initResultModal(text) {
	$("#result_modal_loader").addClass("active")

	$("#result_modal_loader_text").text(text)
	$("#result_modal_header").text("Please wait")
	$("#result_modal_message").text("")
	$("#result_modal_button").html('Do in Background<i class="mail forward icon"></i>')
}

// alter the result modal
function alterResultModal(title, message) {
	$("#result_modal_header").text(title)
	$("#result_modal_message").text(message)
	$("#result_modal_button").html('OK<i class="checkmark icon"></i>')

	$("#result_modal_loader").removeClass("active")
}

// init the progressModal()
function initProgressModal() {
	$('#progress_modal_bar').progress({
		percent: 0
	});
	
	$("#progress_modal_bar").css("display", "")
	$("#progress_modal_bar_message").text("Uploading to Server")
	$("#progress_modal_message").text("")
	$("#progress_modal_button").html('Do in Background<i class="mail forward icon"></i>')
}

// alter the progress modal
function alterProgressModal() {
	$("#progress_modal_bar").css("display", "none")
	$("#progress_modal_message").text("Success!")
	$("#progress_modal_button").html('OK<i class="checkmark icon"></i>')
}
