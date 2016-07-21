import datetime 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import render

from django.utils.timezone import utc
from django.contrib.auth import authenticate

from mainapp.models import Document, Job, CodeFile, Result
from mainapp.serializers import DocumentSerializer1, DocumentSerializer2, JobSerializer1, JobSerializer2, CodeFileSerializer1
from mainapp.permissions import IsOwnerOrReadOnly, checkPermissionAndExistence
		

class DocumentList(APIView):
	"""
	view all documents (for current user) & add a document
	"""
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		doucments = Document.objects.filter(owner=request.user)
		serializer = DocumentSerializer1(doucments, many=True)
		return Response({"result": "success", "message": "none", "data": serializer.data},
			headers={"Access-Control-Allow-Origin": "*"})

	def post(self, request, format=None):
		serializer = DocumentSerializer2(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			return Response({"result": "success", "message": "none", "data": serializer.data},
				headers={"Access-Control-Allow-Origin": "*"})

		return Response({"result": "fail", "message": "your submission has error(s)", "data": serializer.errors}, 
			status=status.HTTP_400_BAD_REQUEST,
			headers={"Access-Control-Allow-Origin": "*"})

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		serializer.save(owner=now_user, upload_time=now_time, size=-1)


class DocumentDetail(APIView):
	"""
	retrieve/delete a Document
	"""
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self, pk):
		try:
			return Document.objects.get(pk=pk)
		except Document.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		document = self.get_object(pk)
		result = checkPermissionAndExistence(document, request.user) 
		if result is not None:
			return result
		else:
			serializer = DocumentSerializer1(document)
			return Response({"result": "success", "message": "none", "data": serializer.data},
				headers={"Access-Control-Allow-Origin": "*"})

	def delete(self, request, pk, format=None):
		document = self.get_object(pk)
		result = checkPermissionAndExistence(document, request.user) 
		if result is not None:
			return result
		else:
			document.delete()
			return Response({"result": "success", "message": "none"}, 
				headers={"Access-Control-Allow-Origin": "*"},)


class JobList(APIView):
	"""
	view all jobs (for current user) & add a job
	"""
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		jobs = Job.objects.filter(owner=request.user)
		# jobs = Job.objects.all()
		serializer = JobSerializer1(jobs, many=True)
		return Response({"result": "success", "message": "none", "data": serializer.data},
			headers={"Access-Control-Allow-Origin": "*"})

	def post(self, request, format=None):
		serializer = JobSerializer2(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			return Response({"result": "success", "message": "none", "data": serializer.data},
				headers={"Access-Control-Allow-Origin": "*"})
		return Response({"result": "fail", "message": "your submission has error(s)", "data": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST,
			headers={"Access-Control-Allow-Origin": "*"})

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		serializer.save(owner=now_user, start_time=now_time, status="running", spark_job_id=-1)


class JobDetail(APIView):
	"""
	retrieve/delete a Job
	"""
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self, pk):
		try:
			return Job.objects.get(pk=pk)
		except Job.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		job = self.get_object(pk)
		result = checkPermissionAndExistence(job, request.user) 
		if result is not None:
			return result
		else:
			serializer = JobSerializer1(job)
			return Response({"result": "success", "message": "none", "data": serializer.data},
				headers={"Access-Control-Allow-Origin": "*"})

	def delete(self, request, pk, format=None):
		job = self.get_object(pk)
		result = checkPermissionAndExistence(job, request.user) 
		if result is not None:
			return result
		else:
			job.delete()
			return Response({"result": "success", "message": "none"}, 
				headers={"Access-Control-Allow-Origin": "*"})
