from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
	name = models.CharField(max_length=100)
	upload_time = models.DateTimeField('time uploaded')
	size = models.IntegerField(default=0)
	description = models.CharField(max_length=250, null=True)
	owner = models.ForeignKey('auth.User', related_name="documents")

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class Job(models.Model):
	name = models.CharField(max_length=50)
	start_time = models.DateTimeField('time started')
	end_time = models.DateTimeField('time ended', null=True)
	status = models.CharField(max_length=20)
	description = models.CharField(max_length=250, null=True)
	spark_job_id = models.CharField(max_length=100)
	owner = models.ForeignKey('auth.User', related_name="jobs")
	parameters = models.CharField(max_length=230, null=True)
	code_files = models.ManyToManyField(Document)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class Result(models.Model):
	path = models.CharField(max_length=100)
	job = models.ForeignKey(Job, related_name="results")
