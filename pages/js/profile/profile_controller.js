profile.controller("profileController", ['$scope', 'profileService', function($scope, profileService) {
	var self = this

	self.jobs = []
	self.viewing_job =  null
	self.viewing_files = []
	self.locs = []
	self.current_parent_url = ""
	self.viewing_file = null

	self.getAllJobs = function() {
		$("#job_dimmer").addClass('active')

		profileService.getAllJobs()
			.then(
				function(data) {
					for (var i = 0; i < data.length; i++) {
						if (data[i]["status"] == "KILLING" || data[i]["status"] == "KILLED") {
							data[i]["status_num"] = -1;
						} else if (data[i]["status"] == "FINISHED") {
							data[i]["status_num"] = 1;
						} else {
							data[i]["status_num"] = 0;
						}

						if (data[i]["status"] == "FINISHED" || data[i]["status"] == "FAILED" || data[i]["status"] == "KILLED") {
							data[i]["status_num_2"] = 1;
						} else if (data[i]["status"] != "KILLING") {
							data[i]["status_num_2"] = 0;
						}
					}

					self.jobs = data

					$("#job_dimmer").removeClass('active')
				},
				function(error) {

				}
			)
	}

	self.getJob = function(job_id) {
		$("#detail_modal_loader").addClass("active")

		$("#job_detail_modal").modal("show")

		profileService.getJobById(job_id)
			.then(
				function(data) {
					self.viewing_job = data

					$("#detail_modal_loader").removeClass('active')
				},
				function(error) {

				}
			)
	}

	self.deleteJob = function(job_id) {
		initResultModal("Deleting")

		$('#public_result_modal').modal('setting', 'closable', false).modal('show')

		profileService.deleteJobById(job_id)
			.then(
				function(data) {
					alterResultModal("Success", "The job has been deleted successfully")

					self.getAllJobs()
				},
				function(data) {

				}
			)
	}

	self.abortJob = function(job_id) {
		initResultModal("Aborting")

		$('#public_result_modal').modal('setting', 'closable', false).modal('show')

		profileService.abortJobById(job_id)
			.then(
				function(data) {
					alterResultModal("Success", "The job is being aborted, please wait")

					self.getAllJobs()
				},
				function(data) {
					
				}
			)
	}

	self.startJob = function() {
		initResultModal("Starting")

		$('#public_result_modal').modal('setting', 'closable', false).modal('show')

		var job_data = $("#job_start_form").serialize()
		profileService.startJob(job_data)
			.then(
				function(data) {
					alterResultModal("Success", "The job has been started successfully")

					self.getAllJobs()
				},
				function(data) {
					
				}
			)
	}


	self.getHomeFiles = function() {
		profileService.getHomeDir()
			.then(
				function(data) {
					self.getSubFiles(false, false, "home", data["pk"])
				},
				function(data) {
					
				}
			)
	}

	self.getSubFiles = function(is_backing, is_refreshing, dir_name, dir_id) {
		$("#document_dimmer").addClass('active')

		if (is_refreshing) {
			dir_id = self.locs[self.locs.length-1].id
		}

		profileService.getSubFilesById(dir_id)
			.then(
				function(data) {
					self.viewing_files = data
					
					if (!is_refreshing) {
						if (is_backing) {
							while (self.locs[self.locs.length-1].id != dir_id) {
								self.locs.pop()
							}
						} else {
							self.locs.push({
								name: dir_name,
								id: dir_id
							})
						}

						self.current_parent_url = 'http://' + CURRENT_URL + ':8000/fs/file/' + dir_id + '/'
					}
					
					$("#document_dimmer").removeClass('active')
				},
				function(data) {
					
				}
			)
	}

	self.uploadFile = function() {
		initProgressModal()

		$('#document_upload_progress_modal').modal('setting', 'closable', false).modal('show')

		var formData = new FormData($("form")[1]);

		profileService.uploadFile(formData)
			.then(
				function(data) {
					alterProgressModal()

					// refresh
					self.getSubFiles(false, true, "", -1)
				},
				function(data) {
					
				}
			)
	}

	self.deleteFile = function(file_id) {
		initResultModal("Deleting")

		$('#public_result_modal').modal('setting', 'closable', false).modal('show')

		profileService.deleteFileById(file_id)
			.then(
				function(data) {
					alterResultModal("Success", "The file has been deleted successfully")

					// refresh
					self.getSubFiles(false, true, "", -1)
				},
				function(data) {
					
				}
			)
	}

	self.getFile = function(file_id) {
		$("#detail_modal_loader_2").addClass("active")

		$("#file_detail_modal").modal("show")

		profileService.getFileById(file_id)
			.then(
				function(data) {
					self.viewing_file = data

					$("#detail_modal_loader_2").removeClass('active')
				},
				function(error) {

				}
			)
	}

	// init
	self.getAllJobs()
	self.getHomeFiles()
}])
