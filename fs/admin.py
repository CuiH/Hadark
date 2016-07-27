from django.contrib import admin
from .models import File

# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """
    Control the display of File object.
    """
    list_display = ('owner', 'name', 'file_type')
