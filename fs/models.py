from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .basis import make_dir, delete_object
# Create your models here.

class File(models.Model):
    """
    A logic file instance for operations.
    """
    TYPE_CHOICE   = {
        ('DIR', 'directory'),
        ('FILE', 'file'),
    }
    owner         = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='upload_file')
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
        """
        Return the absolute path of this file instance in hdfs.
        """
        temp = self
        hdfs_path = ""
        while temp != None:
            hdfs_path = "/" + temp.name + hdfs_path
            temp = temp.parent
        if len(hdfs_path) > 2:
            return hdfs_path[2:]
        else:
            return hdfs_path[1:]

    def get_sub_file(self):
        """
        Return sub File instances whose parent node is this instance.
        """
        sub_file = self.parent_node.all()
        return sub_file

def delete_user_file_in_hdfs(user):
    """
    Remove user's all file in hdfs.
    """
    file_set = user.upload_file.all()
    for item in enumerate(file_set):
        if item[1].file_type == 'FILE':
            hdfs_path = item[1].get_hdfs_path()
            username = user.username
            delete_object(username, hdfs_path)


def get_home_dir(user):
    """
    Return the home File instance of a user
    """
    username = user.username
    root_dir = File.objects.filter(parent=None)[0]
    user_dir = root_dir.parent_node.filter(name='user')[0]
    home_dir = user_dir.parent_node.filter(name=username)[0]
    return home_dir

@receiver(post_save, sender=User)
def create_user_dir(sender, instance, created, **kwargs):
    """
    Create corresponding File instance and directory in hdfs
    when a user is created
    """
    if created:
        root_dir = File.objects.filter(parent=None)[0]
        user_dir = root_dir.parent_node.filter(name='user')[0]
        home_dir = File.objects.create(owner=instance, name=instance.username, parent=user_dir)
        response = make_dir(instance.username, home_dir.get_hdfs_path())
        print(response)

@receiver(pre_delete, sender=User)
def remove_user_dir(sender, instance, using, **kwargs):
    """
    Remove corresponding File instance and directory in hdfs
    when a user is deleted
    """
    home_dir = get_home_dir(instance)
    delete_user_file_in_hdfs(instance)
    response = delete_object(instance.username, home_dir.get_hdfs_path())
    print(response)
    home_dir.delete()
