from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename="user")

urlpatterns = [    
    path('users/reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
    path('login/', views.user_login),
    path('admins/shipping/', views.shipping_admin),
    path('admins/bay/', views.bay_admin),
    path('otp/verify/', views.otp_verification),
    path('otp/new/', views.reset_otp),
    path("users/<uuid:user_id>/suspend/", views.suspend_user),
    path("users/<uuid:user_id>/unsuspend/", views.unsuspend_user),
    
]
