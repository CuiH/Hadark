$(document).ready(function(){
	// init semantic
	$('.menu .item').tab()
	$('select.dropdown').dropdown()

	// init data
	// getAllDocuments()
	getAllJobs()

	// show the upload_document modal
	$("#upload_document").click(function() {
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

	// get file name from input_file
	var getFileName = function(filePath) {
		var p1 = filePath.lastIndexOf('/')
		var p2 = filePath.lastIndexOf('\\')
		var pos = Math.max(p1, p2)
		return filePath.substring(pos+1)
	}

	// synchronize file_name field
	$("#document_upload_file").change(function() {
		$("#document_upload_name").val(getFileName($(this).val()))
	})

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

	// get all documents
	function getAllDocuments() {
		$("#document_dimmer").addClass('active')

		$.ajax({
			type:"get",
			url:"http://172.18.231.84:8000/api/documents",
			headers: {
				"Authorization": "Basic " + btoa("cuihao:admin123")
			},
			success: function(data) {
				var documents = data["detail"]

				$("#document_body").html("");

				for (var i = 0; i < documents.length; i++) {
					var str =		'<tr>' +
									'<td>' + documents[i]["name"] + '</td>' +
									'<td>' + documents[i]["upload_time"] + '</td>' +
									'<td>' + documents[i]["size"] + '</td>'
					if (documents[i]["status"] == "uploading") {
						str += 		'<td>' +
										'<i class="large yellow attention icon"></i>' +
									'</td>'
					} else if (documents[i]["status"] == "uploaded") {
						str += 		'<td>' +
										'<i class="large green checkmark icon"></i>' +
									'</td>'
					} else {
						str += 		'<td>' +
										'<i class="large red icon close"></i>' +
									'</td>'
					}
					str +=				'<td class="right aligned"><div class="teal ui small button">View </div></td>' +
									'<td class="right aligned"><div class="red ui small button">Delete </div></td>' +
								'</tr>'
							
					$("#document_body").append(str)
				}

				$("#document_dimmer").removeClass('active')
			}
		});
	}
	
	// get all jobs
	function getAllJobs() {
		$("#job_dimmer").addClass('active')

		$.ajax({
			type:"get",
			url:"http://172.18.231.84:8000/api/jobs",
			headers: {
				"Authorization": "Basic " + btoa("hwb:hwb")
			},
			success: function(data) {
				var jobs = data["detail"]

				$("#job_body").html("");

				for (var i = 0; i < jobs.length; i++) {
					var str =		'<tr>' +
									'<td>' + jobs[i]["name"] + '</td>' +
									'<td>' + jobs[i]["start_time"] + '</td>' +
									'<td>' + jobs[i]["end_time"] + '</td>'
					
					if (jobs[i]["status"] == "FINISHED") {
						str += 		'<td>' +
										'<i class="large green checkmark icon"></i>FINISHED' +
									'</td>'
					} else if (jobs[i]["status"] == "KILLING" || jobs[i]["status"] == "KILLED") {
						str += 		'<td>' +
										'<i class="large red icon close"></i>' + jobs[i]["status"] + 
									'</td>'
					} else {
						str += 		'<td>' +
										'<i class="large yellow attention icon"></i>' + jobs[i]["status"] + 
									'</td>'
					}
					str +=				'<td class="right aligned"><div class="teal ui small button">View </div></td>' +
									'<td class="right aligned"><div class="red ui small button">Delete </div></td>' +
								'</tr>'
							
					$("#job_body").append(str)
				}

				$("#job_dimmer").removeClass('active')
			}
		});
	}

	// upload file to server
	$("#document_upload_button").click(function() {
		$('#progress_modal_bar').progress({
			percent: 0
		});

		$("#progress_modal_bar").css("display", "")
		$("#progress_modal_bar_message").text("Uploading to Server")
		$("#progress_modal_message").text("")
		$("#progress_modal_button").html('Do in Background<i class="mail forward icon"></i>')

		$('#document_upload_progress_modal').modal('setting', 'closable', false).modal('show')

		var formData = new FormData($("form")[1]);

		$.ajax({
			url: "http://172.18.231.84:8000/api/documents",
			type: "post",
			data: formData,
			cache: false,
			contentType: false,
			processData: false,
			headers: {
				"Authorization": "Basic " + btoa("cuihao:admin123")
			},
			xhr: function(){
				var xhr = $.ajaxSettings.xhr();
				if(onprogress && xhr.upload) {
					xhr.upload.addEventListener("progress" , onprogress, false);
					return xhr;
				}
			},
			success: function(data) {
				$("#progress_modal_bar").css("display", "none")
				$("#progress_modal_message").text("Success!")
				$("#progress_modal_button").html('OK<i class="checkmark icon"></i>')

				getAllDocuments()
			}, 
			complete: function(xhr) {

			} 
		})
	})

	$("#job_start_button").click(function() {
		$("#loading_modal_loader").addClass("active")
		$("#loading_modal_message").text("")
		$("#loading_modal_button").html('Do in Background<i class="mail forward icon"></i>')

		$('#job_start_loading_modal').modal('setting', 'closable', false).modal('show')

		$.ajax({
			url: "http://localhost:8000/api/jobs",
			type: "post",
			data: $("#job_start_form").serialize(),
			headers: {
				"Authorization": "Basic " + btoa("hwb:hwb")
			},
			success: function(data) {
				$("#loading_modal_loader").removeClass("active")
				$("#loading_modal_message").text("Success!")
				$("#loading_modal_button").html('OK<i class="checkmark icon"></i>')

				getAllJobs()
			}, 
			complete: function(xhr) {

			} 
		})
	})
})
