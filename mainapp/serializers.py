from rest_framework import serializers

from mainapp.models import Job, Result

from fs.models import File
from fs.serializer import FileSerializer


class CodeFileSerializer1(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = ('id', 'name', 'size')


class JobSerializer1(serializers.ModelSerializer):
	"""
	used in viewing a job
	"""
	code_files = CodeFileSerializer1(read_only=True, many=True)

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
		file_id = validated_data.pop("code_files")
		doc = File.objects.get(pk=file_id)
		job = Job.objects.create(**validated_data)
		job.code_files.add(doc)

		return job
