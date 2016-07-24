from django.conf.urls import url

from file_management import views

urlpatterns = [
	url(r'^(?P<filename>[^/]+)$', views.FileView.as_view(), name="file_management"),
]
