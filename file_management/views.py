import datetime
import os

from django.shortcuts import render
from django.utils.timezone import utc
from django.http import HttpResponse
from django.views.generic import View

from rest_framework import status, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from mainapp.models import Document


class FileRetrieve(APIView):
	"""
	file retrieve
	"""

	permission_classes = (IsAuthenticated,)
	
	def get(self, request, filename, format=None):
		try:
			Document.objects.get(name=filename)
		except Document.DoesNotExist:
			return Response({"detail": "no such document"},
				status=status.HTTP_404_NOT_FOUND)

		# download file from hadoop

		file_token = generate_token()
		file_path = "/home/cuih/ttt2/" + file_token + "_" + filename

		return Response({"detail": file_token})
		
	def generate_token(self):
		return "1"
		# return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))


class FileDownload(View):
	"""
	file download
	"""

	def get(self, request, filetoken, filename, format=None):
		file_path = "/home/vinzor/tmp_files/download" + filetoken + '_' + filename
		if not os.path.exists(file_path):
			return Response({"detail": "no such document"},
				status=status.HTTP_404_NOT_FOUND)
		
		return HttpResponse(self.read_file(file_path))

	def read_file(self, file_path, buf_size=22222):
		f = open(file_path, "rb")
		while True:
			c = f.read(buf_size)
			if c:
				yield c
			else:
				break

		f.close()
