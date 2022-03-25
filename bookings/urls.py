from django.urls import path
from . import views


urlpatterns = [
    path('new/', views.booking),
    path('', views.get_booking),
    path('mine/', views.user_booking),
    path('<uuid:booking_id>/', views.booking_detail),
    path('mark_complete/', views.booking_complete),
]
