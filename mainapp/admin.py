from django.contrib import admin

from mainapp.models import Document, Job, CodeFile, Result


class CodeFileInline(admin.StackedInline):
	model = CodeFile
	extra = 1


class JobAdmin(admin.ModelAdmin):
	inlines = [CodeFileInline]


admin.site.register(Document)
admin.site.register(Job, JobAdmin)
admin.site.register(CodeFile)
admin.site.register(Result)
