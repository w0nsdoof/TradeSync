from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, AdminOnlyView, TraderOnlyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # Test RBAC
    path("admin/", AdminOnlyView.as_view(), name="admin-only"),
    path("trader/", TraderOnlyView.as_view(), name="trader-only"),
]
