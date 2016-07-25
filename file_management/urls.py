from django.conf.urls import url

from file_management import views

urlpatterns = [
	url(r'^retrieve/(?P<filename>[^/]+)$', views.FileRetrieve.as_view(), name="file_retrieve"),
	url(r'^download/(?P<filetoken>[^/]+)/(?P<filename>[^/]+)$', views.FileDownload.as_view(), name="file_download"),
]
