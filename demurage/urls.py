from django.urls import path
from . import views

urlpatterns = [
    path("rates/", views.demurage),
    path("rates/<rate_id>", views.demurage_detail),
    path("sizes/", views.demurage_sizes),
    path("sizes/<size_id>", views.demurage_size_detail),
    path("calculator/", views.calculate_demurage)
]

