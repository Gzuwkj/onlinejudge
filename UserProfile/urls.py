from django.conf.urls import url
from . import views
app_name = 'user'

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^info/(?P<uid>\d+)/$', views.userinfo_view, name='info'),
    url(r'^rank/', views.user_rank, name='user_rank'),
]
