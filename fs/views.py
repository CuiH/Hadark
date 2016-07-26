from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import *
from datetime import datetime
from .serializer import FileSerializer, UserSerializer
from .models import File
from .basis import *
# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'home':
            user = self.request.user
            username = user.username
            root_dir = File.objects.filter(parent=None)[0]
            user_dir = root_dir.parent_node.filter(name='user')[0]
            home_dir = user_dir.parent_node.filter(name=user.username)[0]
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

        instance = serializer.save(owner=self.request.user, modified=datetime.now())

        username = self.request.user.username
        hdfs_path = instance.get_hdfs_path()
        if data['file_type'] == 'FILE':
            local_file = instance.file_uploaded.path
            upload_file(username, local_file, hdfs_path)
            delete_uploaded_file(local_file)
            serializer.save(file_uploaded=None)
        elif data['file_type'] == 'DIR':
            make_dir(username, hdfs_path)


    def perform_update(self, serializer):
        """
        Recursively update modified field, not implemented yet.
        Only file name should be updated manually.
        """
        origin_instance = self.get_object()
        old_path = origin_instance.get_hdfs_path()

        new_instance = serializer.save(modified=datetime.now())
        new_path = new_instance.get_hdfs_path()
        username = self.request.user.username
        # rename a file
        if old_path != new_path:
            rename_object(username, old_path, new_path)

    def perform_destroy(self, instance):
        """
        Remove a file or directory in hdfs.
        """
        username = self.request.user.username
        hdfs_path = instance.get_hdfs_path()
        delete_object(username, hdfs_path)
        instance.delete()
        print("perform_destroy finish")

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
