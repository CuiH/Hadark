from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'file_type')
