from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.submit_search, name='index'),
    #url(r'^search_results/', views.submit_search),
]
