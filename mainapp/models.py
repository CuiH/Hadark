from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.timezone import utc

from almee.action import action

from fs.models import File


class Job(models.Model):
	name = models.CharField(max_length=50)
	start_time = models.DateTimeField('time started')
	end_time = models.DateTimeField('time ended', null=True)
	status = models.CharField(max_length=20)
	description = models.CharField(max_length=250, null=True)
	spark_job_id = models.CharField(max_length=100)
	owner = models.ForeignKey('auth.User', related_name="jobs")
	parameters = models.CharField(max_length=230, null=True)
	code_files = models.ManyToManyField(File)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def check_status(self):
		old_status = self.status
		if old_status in ["ACCEPTED", "RUNNING", "KILLING"]:
			ac = action()
			new_status = ac.getStatus(self.spark_job_id)['State']
			if old_status != new_status:
				self.update_partially(status=new_status)
				if new_status in ["FAILED", "FINISHED"]:
					now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
					self.update_partially(end_time=now_time)

	def update_partially(self, **args):
		for key in args:
			if key == 'status':
				self.status = args[key]
			if key == 'spark_job_id':
				self.spark_job_id = args[key]
			if key == 'end_time':
				self.end_time = args[key]

		self.save()

class Result(models.Model):
	path = models.CharField(max_length=100)
	job = models.ForeignKey(Job, related_name="results")
