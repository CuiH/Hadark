from django.conf.urls import url
from mainapp import views

urlpatterns = [
	url(r'^jobs$', views.JobList.as_view(), name="all_job"),
	url(r'^job/(?P<pk>[0-9]+)$', views.JobDetail.as_view(), name="job"),
	url(r'^documents$', views.DocumentList.as_view(), name="all_document"),
	url(r'^document/(?P<pk>[0-9]+)$', views.DocumentDetail.as_view(), name="document"),
]
