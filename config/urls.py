from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include("apps.users.urls")),
    path('api/products/', include("apps.products.urls")),
    path('api/trading/', include("apps.trading.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)