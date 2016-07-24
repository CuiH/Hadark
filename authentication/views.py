import datetime 

from django.utils.timezone import utc
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from authentication.serializers import UserSerializer1
from mainapp.permissions import checkAdmin


class UserList(APIView):
	"""
	view all users
	"""

	permission_classes = (IsAdminUser,)
	
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer1(users, many=True)
		return Response({"detail": serializer.data})


class LogonView(APIView):
	"""
	handle user logon
	"""

	def get_user(self, username):
		try:
			return User.objects.get(username=username)
		except User.DoesNotExist:
			return None

	def post(self, request, format=None):
		result = self.check_valid(request)
		if result is not None:
			return result
		
		new_user = self.perform_create(request)
		serializer = UserSerializer1(new_user)

		return Response({"detail": serializer.data})

	def check_valid(self, request):
		if not request.data.has_key("username"):
			return Response({"detail": "please enter a username"}, 
				status=status.HTTP_400_BAD_REQUEST)

		# check duplicate username
		if self.get_user(request.data["username"]) is not None:
			return Response({"detail": "this username has been used"}, 
				status=status.HTTP_400_BAD_REQUEST)

		if not request.data.has_key("password"):
			return Response({"detail": "please enter a password"}, 
				status=status.HTTP_400_BAD_REQUEST)

		return None


	def perform_create(self, request):
		# last_login = date_joined
		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		new_user = User.objects.create_user(request.data["username"], "", request.data["password"])
		new_user.last_login = now_time;
		new_user.save()

		return new_user


class LoginView(APIView):
	"""
	handle user login
	"""

	def post(self, request, format=None):
		result = self.check_valid(request)
		if result is not None:
			return result

		user = authenticate(username=request.data['username'], password=request.data['password'])
		if user is not None:
			if user.is_active:
				# update last login
				now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
				user.last_login = now_time
				user.save()
				serializer = UserSerializer1(user)

				return Response({"detail": serializer.data})

			return Response({"detail": "not active"},
				status=status.HTTP_400_BAD_REQUEST)

		return Response({"detail": "wrong username or password"},
			status=status.HTTP_400_BAD_REQUEST)

	def check_valid(self, request):
		if not request.data.has_key("username"):
			return Response({"detail": "please enter a username"}, 
				status=status.HTTP_400_BAD_REQUEST)

		if not request.data.has_key("password"):
			return Response({"detail": "please enter a password"}, 
				status=status.HTTP_400_BAD_REQUEST)

		return None
