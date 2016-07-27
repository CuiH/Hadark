import os
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import FileSerializer, UserSerializer
from .models import File
from .basis import upload_file, delete_object, rename_object, open_file, make_dir
# Create your views here.


def get_home_dir(user):
    """
    Return the home File instance of a user.
    """
    username = user.username
    root_dir = File.objects.filter(parent=None)[0]
    user_dir = root_dir.parent_node.filter(name='user')[0]
    home_dir = user_dir.parent_node.filter(name=username)[0]
    return home_dir


class FileViewSet(viewsets.ModelViewSet):
    """

    """
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        """
        Return File instance which belongs to the current user.
        Query params: sub_file=pk, return child instance of the File instance.
        """
        current_user = self.request.user
        queryset = File.objects.filter(owner=current_user)
        sub_file = self.request.query_params.get('sub_file', None)
        if sub_file is not None:
            queryset = queryset.filter(pk=sub_file)
            node = None
            if len(queryset):
                node = queryset[0]
                return node.get_sub_file()
            else:
                return node
        return queryset

    def get_object(self):
        """
        Return an File instance based on pk
        if pk == home, return home File instance
        """
        pk = self.kwargs.get('pk')
        if pk == 'home':
            user = self.request.user
            home_dir = get_home_dir(user)
            return home_dir
        return super(FileViewSet, self).get_object()

    def perform_create(self, serializer):
        """
        Upload file to hdfs or create directory in hdfs
        """
        size = 0
        data = serializer.validated_data

        if data['file_type'] == 'FILE':
            size = self.request.FILES['file_uploaded'].size

        instance = serializer.save(owner=self.request.user, modified=timezone.now(), size=size)

        username = self.request.user.username

        hdfs_path = instance.get_hdfs_path()
        if data['file_type'] == 'FILE':
            local_file = instance.file_uploaded.path
            response = upload_file(username, local_file, hdfs_path)
            os.remove(local_file)

            if response != 'Upload success':
                print("upload file fail!")
                instance.delete()
                raise serializers.ValidationError({
                    'hdfs_path': response
                })

            serializer.save(file_uploaded=None)
        elif data['file_type'] == 'DIR':
            response = make_dir(username, hdfs_path)
            if response != 'Create directory success':
                instance.delete()
                print("create directory fail!")
                raise serializers.ValidationError({
                    'hdfs_path': response
                })

    def perform_update(self, serializer):
        """
        Recursively update modified field, not implemented yet.
        Only file name should be updated currently.
        """
        origin_instance = self.get_object()
        old_path = origin_instance.get_hdfs_path()
        old_name = origin_instance.name
        old_modified = origin_instance.modified

        new_instance = serializer.save(modified=timezone.now())
        new_path = new_instance.get_hdfs_path()
        username = self.request.user.username
        # rename a file
        response = None
        if old_path != new_path:
            response = rename_object(username, old_path, new_path)

        if response == 'fail':
            print("rename fail")
            serializer.save(name=old_name, modified=old_modified)
            raise serializers.ValidationError({
                'new_path': 'object already existed'
            })

    def perform_destroy(self, instance):
        """
        Remove a file or directory in hdfs.
        """
        username = self.request.user.username
        hdfs_path = instance.get_hdfs_path()
        response = delete_object(username, hdfs_path)
        if response != 'Remove object success':
            print("Remove fail!")
            raise serializers.ValidationError({
                'hdfs_path': response
            })
        instance.delete()

@api_view(['GET'])
def get_file_content(request):
    """
    Retrieve file in hdfs.
    """
    params = request.query_params
    username = params['username']
    hdfs_path = params['path']
    content = open_file(username, hdfs_path)
    return Response({"content": content})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
