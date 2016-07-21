from django.conf.urls import url
from mainapp import views

urlpatterns = [
	url(r'^jobs$', views.JobView.as_view(), name="all_jobs"),
	url(r'^documents$', views.DocumentView.as_view(), name="all_document"),
]
