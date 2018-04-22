from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token


admin.site.site_header = settings.SITE_ADMIN_TITLE

router = routers.DefaultRouter()

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^api/login/', obtain_jwt_token),

    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
