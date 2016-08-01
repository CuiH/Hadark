from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth.models import AnonymousUser


class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		
		return obj.owner == request.user


def checkPermissionAndExistence(obj, current_user):
	custom_headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Authorization"}

	print(current_user)
	if obj.owner != current_user:
		return Response({"result": "fail", "message": "you have no access to this object(s)"}, 
			headers=custom_headers,
			status=status.HTTP_403_FORBIDDEN)

	if obj is None:
		return Response({"result": "fail", "message": "no such object"}, 
			headers=custom_headers,
			status=status.HTTP_400_BAD_REQUEST)

	return None


def checkAdmin(current_user):
	custom_headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Authorization"}

	if not current_user.is_staff:
		return Response({"result": "fail", "message": "you have no access to this object(s)"}, 
			headers=custom_headers,
			status=status.HTTP_403_FORBIDDEN)

	return None


def checkAuthenticated(current_user):
	custom_headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Authorization"}

	if isinstance(current_user, AnonymousUser):
		return Response({"result": "fail", "message": "you have no access to this object(s)"}, 
			headers=custom_headers,
			status=status.HTTP_401_UNAUTHORIZED)

	return None
