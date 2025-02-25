from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include("apps.users.urls")),
    path('api/products/', include("apps.products.urls")),
    path('api/trading/', include("apps.trading.urls")),
]
