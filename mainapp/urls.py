from django.conf.urls import url, include
from mainapp import views

urlpatterns = [
	url(r'^jobs$', views.JobList.as_view(), name="all_job"),
	url(r'^job/(?P<pk>[0-9]+)$', views.JobDetail.as_view(), name="job")
]
