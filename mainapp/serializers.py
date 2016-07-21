from rest_framework import serializers

from mainapp.models import Document, Job, CodeFile, Result


class DocumentSerializer1(serializers.ModelSerializer):
	"""
	show in user profile page
	"""
	class Meta:
		model = Document
		fields = ('id', 'name', 'upload_time', 'size', 'description')


class DocumentSerializer2(serializers.ModelSerializer):
	"""
	used in adding a document
	"""
	owner = serializers.ReadOnlyField(source='owner.username')
	upload_time = serializers.ReadOnlyField()

	class Meta:
		model = Document
		fields = ('id', 'name', 'upload_time', 'size', 'description', 'owner')


class JobSerializer1(serializers.ModelSerializer):
	"""
	show in user profile page
	"""
	class Meta:
		model = Job
		fields = ('id', 'name', 'start_time', 'end_time', 'status', 'description')


class JobSerializer2(serializers.ModelSerializer):
	"""
	used in adding a job
	"""
	owner = serializers.ReadOnlyField(source='owner.username')
	status = serializers.ReadOnlyField()
	start_time = serializers.ReadOnlyField

	class Meta:
		model = Job
		fields = ('id', 'name', 'owner', 'start_time', 'end_time', 'status', 'description')


class CodeFileSerializer1(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'name', 'uploaded_time')
