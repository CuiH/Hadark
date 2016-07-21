from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import render
from django.contrib.auth.models import User

from mainapp.models import Document, Job, CodeFile, Result
from mainapp.serializers import UserSerializer, DocumentSerializer, JobSerializer, CodeFileSerializer


class UserView(APIView):
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)


class BookView(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, format=None):
		books = Book.objects.all()
		serializer = BookSerializer(books, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = BookSerializer2(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		serializer.save(creater=self.request.user)
