from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^', include('main.urls')),
    url(r'^api/subscribe/', views.SubscribeList.as_view()),
    url(r'^api/workshops/', views.WorkshopsList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

