from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class File(models.Model):
    TYPE_CHOICE   = {
        ('DIR', 'directory'),
        ('FILE', 'file'),
    }
    owner         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name          = models.CharField(max_length=100, null=True)
    file_uploaded = models.FileField(upload_to='file', null=True, blank=True)
    permission    = models.CharField(max_length=10, null=True)
    size          = models.IntegerField(null=True)
    modified      = models.DateTimeField(null=True)
    file_type     = models.CharField(max_length=20, choices=TYPE_CHOICE, default='DIR')
    parent        = models.ForeignKey('File', related_name='parent_node', on_delete=models.CASCADE, null=True, blank=True)
    hdfs_path     = models.CharField(max_length=200, default='/', null=True)
    
    def __str__(self):
        return self.owner.username + ":" + self.name
