import datetime, os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth import authenticate

from mainapp.models import Job, Result
from mainapp.serializers import JobSerializer1, JobSerializer2
from mainapp.permissions import IsOwner

from almee.action import action

from fs.models import File


class JobList(APIView):
	"""
	view all jobs (for current user) & add a job
	"""

	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		jobs = Job.objects.filter(owner=request.user)

		# update from spark
		for job in jobs:
			# job.check_status()
			pass
					
		serializer = JobSerializer1(jobs, many=True)

		return Response({"detail": serializer.data})

	def post(self, request, format=None):
		serializer = JobSerializer2(data=request.data)
		if not serializer.is_valid():
			return Response({"detail": serializer.errors},
				status=status.HTTP_400_BAD_REQUEST)

		# check file's exsistence
		try:
			code_file = File.objects.get(pk=request.data["code_files"])
			
			# check type
			if code_file.file_type != "FILE":
				return Response({"detail": "you should select a file rather than a directory"},
					status=status.HTTP_400_BAD_REQUEST)

			# check owner
			if code_file.owner != request.user:
				return Response({"detail": "you have no access to this document"},
					status=status.HTTP_403_FORBIDDEN)
		except File.DoesNotExist:
			return Response({"detail": "invalid document id"},
				status=status.HTTP_400_BAD_REQUEST)

		# insert into db with status 'starting'
		new_job = self.perform_create(serializer)
		job_id = 0

		# start a spark job
		# ac = action()
		# s_id = ac.submitJob('org.apache.spark.examples.SparkPi', '4g', '4g', '6', 'hdfs:///spark-examples-1.6.2-hadoop2.2.0.jar', '1000')
		# job_id = s_id

		# update job  in db with status 'ACCEPTED'
		new_job.update_partially(spark_job_id=job_id, status='ACCEPTED')
		
		return Response({"detail": JobSerializer1(new_job).data})

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		return serializer.save(owner=now_user, start_time=now_time, status="STARTING", spark_job_id=-1)

	
class JobDetail(APIView):
	"""
	retrieve/delete a Job
	"""

	permission_classes = (IsAuthenticated, IsOwner,)

	def get_object(self, pk):
		try:
			obj = Job.objects.get(pk=pk)
			self.check_object_permissions(self.request, obj)

			return obj
		except Job.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		job = self.get_object(pk)
		if job is not None:
			# update from spark
			job.check_status()

			serializer = JobSerializer1(job)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)

	def put(self, request, pk, format=None):
		''' abort a job '''
		job = self.get_object(pk)
		if job is not None:
			# check status
			if job.status in ["KILLING", "KILLED", "FINISHED", "FAILED"]:
				return Response({"detail": "you can not abort this job"},
					status=status.HTTP_400_BAD_REQUEST)

			# abort in spark
			# ac = action()
			# ac.killApplicationById(job.spark_job_id)

			# update db with status "KILLING"
			now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
			job.update_partially(status="KILLING", end_time=now_time)

			serializer = JobSerializer1(job)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk, format=None):
		job = self.get_object(pk)
		if job is not None:
			# check status
			if job.status in ["RUNNING", "ACCEPTED", "STARTING", "KILLING"]:
				return Response({"detail": "you can not delete this job"},
					status=status.HTTP_400_BAD_REQUEST)
				
			# delete from db
			job.delete()

			return Response({"detail": "none"})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)
