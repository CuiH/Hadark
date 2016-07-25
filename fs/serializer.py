from django.contrib.auth.models import User
from .models import File
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('owner', 'modified', 'size', 'hdfs_path')
