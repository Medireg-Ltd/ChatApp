from apps.accounts.views import robots_txt
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.chat.urls")),
    path("api/schema", SpectacularAPIView.as_view(), name="api_schema"),
    path("api/", SpectacularSwaggerView.as_view(url_name="api_schema")),
    path("robots.txt", robots_txt, name="robots_txt"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
