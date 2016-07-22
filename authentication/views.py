import datetime 

from django.utils.timezone import utc
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from authentication.serializers import UserSerializer1


class UserList(APIView):
	permission_classes = (permissions.IsAdminUser,)

	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer1(users, many=True)
		return Response({"result": "success", "message": "none", "data": serializer.data},
			headers={"Access-Control-Allow-Origin": "*"})


class LogonView(APIView):
	permission_classes = (permissions.AllowAny,)

	def get_object(self, username):
		try:
			return User.objects.get(username=username)
		except User.DoesNotExist:
			return None

	def post(self, request, format=None):
		if self.get_object(request.data["username"]) is not None:
			return Response({"result": "fail", "message": "this username has been used"}, 
				status=status.HTTP_400_BAD_REQUEST,
				headers={"Access-Control-Allow-Origin": "*"})

		now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
		user = User.objects.create_user(request.data["username"], "", request.data["password"])
		user.last_login = now_time;
		user.save()
		serializer = UserSerializer1(user)
		return Response({"result": "success", "message": "none", "data": serializer.data}, 
			headers={"Access-Control-Allow-Origin": "*"})


class LoginView(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		trying_user = request.data
		user = authenticate(username=trying_user['username'], password=trying_user['password'])
		if user is not None:
			if user.is_active:
				# update last login
				now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
				user.last_login = now_time
				user.save()
				serializer = UserSerializer1(user)
				return Response({"result": "success", "message": "none", "data": serializer.data}, 
					headers={"Access-Control-Allow-Origin": "*"})
			else:
				return Response({"result": "fail", "message": "not active"}, 
					headers={"Access-Control-Allow-Origin": "*"},
					status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"result": "fail", "message": "wrong username or password"}, 
				headers={"Access-Control-Allow-Origin": "*"},
				status=status.HTTP_400_BAD_REQUEST)
