import datetime 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import render

from django.utils.timezone import utc
from django.contrib.auth import authenticate

from mainapp.models import Document, Job, CodeFile, Result
from mainapp.serializers import DocumentSerializer1, DocumentSerializer2, JobSerializer1, JobSerializer2, CodeFileSerializer1
from mainapp.permissions import IsOwnerOrReadOnly
		

class DocumentView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		doucments = Document.objects.all()
		serializer = DocumentSerializer1(doucments, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = DocumentSerializer2(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		serializer.save(owner=now_user, upload_time=now_time)


class JobView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		jobs = Job.objects.all()
		serializer = JobSerializer1(jobs, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = JobSerializer2(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		now_user = self.request.user
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		serializer.save(owner=now_user, start_time=now_time, status="running")
