from django.conf.urls import url
from Contest import views
app_name = 'contest'

urlpatterns = [
    url(r'^status/(?P<prob_id>\d+)/$', views.status, name='status'),
    url(r'^(?P<match_id>\d+)/$', views.show_problem, name='show_problem'),
    url(r'^match/$', views.show_contest, name='match'),
    url(r'^rank/$', views.rank, name='rank'),
    url(r'^register/(?P<cid>\d+)/$', views.match_register, name='register_contest'),
    url(r'^check/(?P<run_id>\d+)/$', views.check_code, name='check'),
]