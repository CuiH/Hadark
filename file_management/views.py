import datetime

from django.shortcuts import render
from django.utils.timezone import utc

from rest_framework import status, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# only for test
class FileView(APIView):
	"""
	file upload/download
	"""

	parser_classes =  (parsers.MultiPartParser,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, filename, format=None):
		file_obj = request.data['file']
		path = "/home/cuih/ttt/"
		file_path = path+filename
		des = open(file_path, 'wb+')

		# begin to save to local
		if file_obj.multiple_chunks():
			for chunk in file_obj.chunks():
				des.write(chunk)
		else:
			des.write(file_obj.read())
		des.close()

		return Response({"detail": "none"})
