$(document).ready(function() {
	var height = window.innerHeight - $("#mainContent").offset().top
	$("#mainContent").css("min-height", height + "px")

	$("#feature").click(function() {
		window.location.href = "http://" + CURRENT_URL_2 + "/feature"
	})

	$("#help").click(function() {
		window.location.href = "http://" + CURRENT_URL_2 + "/help";
	})

	$("#logOut").click(function() {
		clearCookie("username")
		clearCookie("password")
		window.location.href = "http://" + CURRENT_URL_2 + "/homepage?login=true"
	})

	// check login
	if (!DEBUG) {
		if (getCookie("username") == null) {
			window.location.href = "http://" + CURRENT_URL_2 + "/homepage?login=true"
		} else {
			$("#userName").text(getCookie("username"))
		}
	} else {
		$("#userName").text("debug")
	}
	
	// init semantic
	$('.menu .item').tab()
	$('select.dropdown').dropdown()

	// show the upload_document modal
	$("#upload_document").click(function() {
		$("#document_upload_file_div").removeAttr("hidden")
		$("#document_upload_type").val("FILE")
		$("#document_upload_name").val("")
		
		$('#document_upload_form_modal').modal({
			blurring: true
		}).modal('show')
	})

	$("#create_folder").click(function() {
		$("#document_upload_type").val("DIR")
		$("#document_upload_file").val("")
		$("#document_upload_name").val("")
		$("#document_upload_file_div").attr("hidden", "")
		
		$('#document_upload_form_modal').modal({
			blurring: true
		}).modal('show')
	})

	// show start_job modal
	$("#start_job").click(function() {
		$('#job_start_form_modal').modal({
			blurring: true
		}).modal('show')
	})
	
	// synchronize file_name field
	$("#document_upload_file").change(function() {
		$("#document_upload_name").val(getFileName($(this).val()))
	})
})
