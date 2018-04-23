from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from apps.workout_tracker.views import WorkoutLogAPIViewSet


admin.site.site_header = settings.SITE_ADMIN_TITLE

api_router = routers.DefaultRouter()
api_router.register(
    r'workout-logs', WorkoutLogAPIViewSet, base_name='workout-logs'
)

urlpatterns = [

    url(r'^api/', include(api_router.urls)),
    url(r'^api/login/', obtain_jwt_token),

    url(r'^admin/', admin.site.urls),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
