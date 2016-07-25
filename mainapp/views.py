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
		print(request.data["file"])
		if not isinstance(request.data["file"], File):
			return Response({"detail": "please upload a file"}, 
				status=status.HTTP_400_BAD_REQUEST)

		# begin to write file to local file system
		file_obj = request.data['file']
		path = "/home/cuih/ttt/" + request.user.username + "/"
		if not os.path.exists(path):
			os.makedirs(path)
		file_path = path + request.data["name"]
		des = open(file_path, 'wb+')
		if file_obj.multiple_chunks():
			for chunk in file_obj.chunks():
				des.write(chunk)
		else:
			des.write(file_obj.read())
		des.close()

		# upload file to hadoop

		# insert into db
		self.perform_create(serializer, file_obj.size)

		return Response({"detail": serializer.data})
		
	def perform_create(self, serializer, file_size):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		serializer.save(owner=now_user, upload_time=now_time, size=file_size)


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
		serializer = JobSerializer1(jobs, many=True)

		return Response({"detail": serializer.data})

	def post(self, request, format=None):
		# doc = Document.objects.get(pk=request.data["code_files"])
		serializer = JobSerializer2(data=request.data)
		if serializer.is_valid():
			new_job = self.perform_create(serializer)

			return Response({"detail": JobSerializer1(new_job).data})

		return Response({"detail": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		job = serializer.save(owner=now_user, start_time=now_time, status="running", spark_job_id=-1)
		return job


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
			serializer = JobSerializer1(job)

			return Response({"detail": serializer.data})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk, format=None):
		job = self.get_object(pk)
		if job is not None:
			job.delete()

			return Response({"detail": "none"})

		return Response({"detail": "no such job"},
			status=status.HTTP_404_NOT_FOUND)
