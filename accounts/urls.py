from django.urls import path, include
from . import views


urlpatterns = [    
    path('users/reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('login/', views.user_login),
    path('admins/shipping/', views.shipping_admin),
    path('admins/bay/', views.bay_admin),
    path('otp/verify/', views.otp_verification),
    path('otp/new/', views.reset_otp),
    path("users/<uuid:user_id>/suspend/", views.suspend_user),
    path("users/<uuid:user_id>/unsuspend/", views.unsuspend_user),
    
]
