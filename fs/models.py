from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from .basis import *
# Create your models here.

class File(models.Model):
    TYPE_CHOICE   = {
        ('DIR', 'directory'),
        ('FILE', 'file'),
    }
    owner         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name          = models.CharField(max_length=100, null=True, blank=True)
    file_uploaded = models.FileField(upload_to='file', null=True, blank=True)
    permission    = models.CharField(max_length=10, null=True)
    size          = models.IntegerField(default=0,null=True)
    modified      = models.DateTimeField(null=True)
    file_type     = models.CharField(max_length=20, choices=TYPE_CHOICE, default='DIR')
    parent        = models.ForeignKey('File', related_name='parent_node', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.get_hdfs_path()

    def get_hdfs_path(self):
        f = self
        hdfs_path = ""
        # /, peter
        while (f != None):
            hdfs_path = "/" + f.name + hdfs_path
            f = f.parent
        if len(hdfs_path) > 2:
            return hdfs_path[2:]
        else:
            return hdfs_path[1:]

@receiver(post_save, sender=User)
def create_user_dir(sender, instance, created, **kwargs):
    """
    Create corresponding File instance when a user is created
    """
    if created:
        root_dir = File.objects.filter(parent=None)[0]
        user_dir = root_dir.parent_node.filter(name='user')[0]
        File.objects.create(owner=instance, name=instance.username, parent=user_dir)

