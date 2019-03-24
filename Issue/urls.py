from django.conf.urls import url
from . import views
app_name = 'problem'

urlpatterns = [
    url(r'^page/(?P<prob_id>\d+)/$', views.problem_page, name='problem_page'),
    url(r'edit/', views.edit, name='edit'),
]
