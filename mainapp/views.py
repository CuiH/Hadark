import datetime, os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth import authenticate
from django.core.files import File

from mainapp.models import Document, Job, Result
from mainapp.serializers import DocumentSerializer1, DocumentSerializer2, JobSerializer1, JobSerializer2
from mainapp.permissions import IsOwner

from almee.action import action
		

class DocumentList(APIView):
	"""
	view all documents (for current user) & add a document
	"""

	permission_classes = (IsAuthenticated,)
	parser_classes =  (parsers.MultiPartParser,)

	def get(self, request, format=None):
		doucments = Document.objects.filter(owner=request.user)
		serializer = DocumentSerializer1(doucments, many=True)

		return Response({"detail": serializer.data})

	def post(self, request, format=None):
		# check other fields first
		serializer = DocumentSerializer2(data=request.data)
		if not serializer.is_valid():
			return Response({"detail": serializer.errors}, 
				status=status.HTTP_400_BAD_REQUEST)

		# check file
		if not isinstance(request.data["file"], File):
			return Response({"detail": "please upload a file"}, 
				status=status.HTTP_400_BAD_REQUEST)

		# insert in to db with status 'uploading'
		file_obj = request.data['file']
		new_document = self.perform_create(serializer, file_obj.size)

		# begin to write file to local file system
		path = "/home/vinzor/tmp_files/upload" + request.user.username + "/"
		if not os.path.exists(path):
			os.makedirs(path)
		file_path = path + request.data["name"]
		sf = self.save_file(file_path, file_obj)
		try:
			while True:
				sf.next()
		except StopIteration:
			pass

		# upload file to hadoop

		# update document in db with new status 'uploaded'
		self.perform_update(new_document, 'uploaded')
		
		return Response({"detail": serializer.data})
		
	def perform_create(self, serializer, file_size):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		return serializer.save(owner=now_user, upload_time=now_time, size=file_size, status="uploading")

	def perform_update(self, doc, doc_status):
		doc.status = doc_status
		doc.save()

	def save_file(self, file_path, file_obj):
		des = open(file_path, 'wb+')
		if file_obj.multiple_chunks():
			for chunk in file_obj.chunks():
				des.write(chunk)
				yield
		else:
			des.write(file_obj.read())
			yield

		des.close()

class DocumentDetail(APIView):
	"""
	retrieve/delete a Document
	"""

	permission_classes = (IsAuthenticated, IsOwner,)

	def get_object(self, pk):
		try:
			obj = Document.objects.get(pk=pk)
			self.check_object_permissions(self.request, obj)

			return obj
		except Document.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		document = self.get_object(pk)
		if document is not None:
			serializer = DocumentSerializer1(document)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such document"},
			status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk, format=None):
		document = self.get_object(pk)
		if document is not None:
			# delete from hadoop

			# delete from db
			document.delete()

			return Response({"detail": "none"})

		return Response({"detail": "no such document"},
			status=status.HTTP_404_NOT_FOUND)
			

class JobList(APIView):
	"""
	view all jobs (for current user) & add a job
	"""

	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		jobs = Job.objects.filter(owner=request.user)

		# update from spark
		for job in jobs:
			if job.status == "running" or job.status == "starting" or job.status:
				pass

		serializer = JobSerializer1(jobs, many=True)

		return Response({"detail": serializer.data})

	def post(self, request, format=None):
		serializer = JobSerializer2(data=request.data)
		if not serializer.is_valid():
			return Response({"detail": serializer.errors},
				status=status.HTTP_400_BAD_REQUEST)

		# check ducument's exsistence
		try:
			document = Document.objects.get(pk=request.data["code_files"])
			# check owner
			if document.owner != request.user:
				return Response({"detail": "you have no access to this documet"},
					status=status.HTTP_403_FORBIDDEN)
		except Document.DoesNotExist:
			return Response({"detail": "invalid document id"},
				status=status.HTTP_400_BAD_REQUEST)

		# insert into db with status 'starting'
		new_job = self.perform_create(serializer)

		# start a spark job
		# ac = action()
		# s_id = ac.submitJob('org.apache.spark.examples.SparkPi', '4g', '4g', '6', 'hdfs:///spark-examples-1.6.2-hadoop2.2.0.jar', '1000')

		# update job  in db with status 'runnning'
		job_id = 0
		self.perform_update(new_job, job_id, 'running')
		
		return Response({"detail": JobSerializer1(new_job).data})

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		return serializer.save(owner=now_user, start_time=now_time, status="starting", spark_job_id=-1)

	def perform_update(self, job, job_id, job_status):
		job.spark_job_id = job_id
		job.status = job_status
		job.save()

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
			if job.status == "running":
				pass

			serializer = JobSerializer1(job)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)

	def put(self, request, pk, format=None):
		''' abort a job '''
		job = self.get_object(pk)
		if job is not None:
			# check status
			if job.status == "aborted" or job.status == "finished":
				return Response({"detail": "invalid action"},
					status=status.HTTP_400_BAD_REQUEST)

			# abort in spark

			# update db
			job.status = "aborted"
			now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
			job.end_time = now_time
			job.save()

			serializer = JobSerializer1(job)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk, format=None):
		job = self.get_object(pk)
		if job is not None:
			# delete from spark

			# delete from db
			job.delete()

			return Response({"detail": "none"})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)
