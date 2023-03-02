from django.urls import path
from . import views

urlpatterns = [
    path("rates/", views.demurage),
    path("rates/<uuid:rate_id>", views.demurage_detail),
    path("sizes/", views.demurage_sizes),
    path("sizes/<uuid:size_id>", views.demurage_size_detail),
    path("calculator/", views.calculate_demurage),
    path("calculations/", views.DemurageCalculationListView.as_view()),
    path("calculations/<int:id>", views.DemurageCalculationDetailView.as_view()),
]

