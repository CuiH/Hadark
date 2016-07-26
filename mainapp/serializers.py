from rest_framework import serializers

from mainapp.models import Document, Job, Result


class DocumentSerializer1(serializers.ModelSerializer):
	"""
	used in viewing a document
	"""
	class Meta:
		model = Document
		fields = ('id', 'name', 'upload_time', 'size', 'description', 'status')


class DocumentSerializer2(serializers.ModelSerializer):
	"""
	used in adding/updating a document
	"""
	owner = serializers.ReadOnlyField(source='owner.username')
	upload_time = serializers.ReadOnlyField()
	size = serializers.ReadOnlyField()
	status = serializers.ReadOnlyField()

	class Meta:
		model = Document
		fields = ('id', 'name', 'upload_time', 'size', 'description', 'owner', 'status')


class JobSerializer1(serializers.ModelSerializer):
	"""
	used in viewing a job
	"""
	code_files = DocumentSerializer1(read_only=True, many=True)

	class Meta:
		model = Job
		fields = ('id', 'name', 'start_time', 'end_time', 'status', 'description', 'parameters', 'code_files')


class JobSerializer2(serializers.ModelSerializer):
	"""
	used in adding a job
	"""
	owner = serializers.ReadOnlyField(source='owner.username')
	status = serializers.ReadOnlyField()
	start_time = serializers.ReadOnlyField()
	spark_job_id = serializers.ReadOnlyField()
	code_files = serializers.IntegerField()

	class Meta:
		model = Job
		fields = ('id', 'name', 'owner', 'start_time', 'end_time', 'status', 'description', 'parameters', 'spark_job_id', 'code_files')

	def create(self, validated_data):
		doc_id = validated_data.pop("code_files")
		doc = Document.objects.get(pk=doc_id)
		job = Job.objects.create(**validated_data)
		job.code_files.add(doc)
		return job



class CodeFileSerializer1(serializers.ModelSerializer):
	job = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Document
		fields = ('id', 'name', 'uploaded_time')
