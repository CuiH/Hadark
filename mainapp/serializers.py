from django.contrib.auth.models import User

from rest_framework import serializers

from mainapp.models import Document, Job, CodeFile, Result


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username')


class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'name', 'upload_time', 'size', 'description')


class JobSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'name', 'start_time', 'end_time', 'status', 'description')


class CodeFileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'name', 'uploaded_time')
