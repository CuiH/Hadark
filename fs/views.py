from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from hadark import settings
from .models import File
from .serializer import *
from .basis import *
import os
# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        size = 0
        data = serializer.validated_data
        parent_path = data['parent'].hdfs_path
        hdfs_path = ''
        if data['file_type'] == 'FILE':
            hdfs_path = parent_path + data['name']
        elif data['file_type'] == 'DIR':
            hdfs_path = parent_path + data['name'] + '/'

        if data['file_type'] == 'FILE' and 'file_uploaded' in self.request.FILES:
            size = self.request.FILES['file_uploaded'].size
            print(type(self.request.FILES['file_uploaded']))

        instance = serializer.save(owner=self.request.user, modified=datetime.now(), size=size, hdfs_path=hdfs_path)

        # upload to hdfs using path field
        username = self.request.user.username
        if data['file_type'] == 'FILE':
            local_file = instance.file_uploaded.path
            upload_file(username, local_file, hdfs_path)
            delete_content(local_file)
        elif data['file_type'] == 'DIR':
            make_dir(username, hdfs_path)


    def perform_update(self, serializer):
        """
        Recursively update modified field, not implemented yet.
        """
        serializer.save(modified=datetime.now())




    def perform_destroy(self, serializer):
        pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
