from django.urls import path
from . import views


urlpatterns = [
    path('new/', views.booking),
    path('', views.get_booking),
    path('mine/', views.user_booking),
    path('<uuid:booking_id>/', views.booking_detail),
    path('verify/', views.verify_booking),
    path('mark_complete/<uuid:booking_id>/', views.booking_complete),
    path("today/pdf/", views.bookings_pdf)
]
