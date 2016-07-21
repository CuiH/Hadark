from rest_framework.response import Response
from rest_framework import status, permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.creater == request.user


def checkPermissionAndExistence(obj, current_user):
	if obj is None:
		return Response({"result": "fail", "message": "no such object"}, 
			headers={"Access-Control-Allow-Origin": "*"},
			status=status.HTTP_400_BAD_REQUEST)

	if obj.owner != current_user:
		print current_user.id
		print obj.owner.username
		return Response({"result": "fail", "message": "you have no access to this object"}, 
			headers={"Access-Control-Allow-Origin": "*"},
			status=status.HTTP_403_FORBIDDEN)

	return None
