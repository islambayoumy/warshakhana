from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<workshop_id>\d+)/$', views.workshop_details, name='details'),
    url(r'^postReq', views.testpostrequest)
]
