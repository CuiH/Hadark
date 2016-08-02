from rest_framework import serializers

from mainapp.models import Job, Result

from fs.models import File
from fs.serializer import FileSerializer

from api.sparkapi import SparkAPI


class CodeFileSerializer1(serializers.ModelSerializer):
	hdfs_path = serializers.SerializerMethodField()
	
	class Meta:
		model = File
		fields = ('id', 'size', 'hdfs_path')

	def get_hdfs_path(self, obj):
		"""
		Return hdfs_path of a File instance
		"""
		return obj.get_hdfs_path()


class JobSerializer1(serializers.ModelSerializer):
	"""
	used in viewing jobs in list
	"""

	class Meta:
		model = Job
		fields = ('id', 'name', 'start_time', 'end_time', 'status')


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
		fields = ('id', 'name', 'owner', 'start_time', 'status', 'description',  'main_class', 'parameters', 'spark_job_id', 'code_files')

	def create(self, validated_data):
		file_id = validated_data.pop("code_files")
		doc = File.objects.get(pk=file_id)
		job = Job.objects.create(**validated_data)
		job.code_files.add(doc)

		return job


class JobSerializer3(serializers.ModelSerializer):
	"""
	used in viewing a job
	"""

	code_files = CodeFileSerializer1(read_only=True, many=True)
	result = serializers.SerializerMethodField()

	class Meta:
		model = Job
		fields = ('id', 'name', 'start_time', 'end_time', 'status', 'description', 'main_class', 'parameters', 'code_files', 'result')

	def get_result(self, obj):
		if obj.status in ["FINISHED", "FAILED"]:
			result = {}
			sa = SparkAPI()
			logs = sa.getLog(obj.spark_job_id)
			if obj.status == "FINISHED":
				for key in logs:
					result[key] = logs[key][1]
			elif obj.status == "FAILED":
				for key in logs:
					result[key] = logs[key][0]

			return result
		else:
			return "none"
