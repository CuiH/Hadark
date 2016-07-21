from django.conf.urls import url
from authentication import views

urlpatterns = [
	url(r'^users$', views.UserList.as_view(), name="all_user"),
	url(r'^login$', views.LoginView.as_view(), name="login"),
	url(r'^logon$', views.LogonView.as_view(), name="logon"),
]
