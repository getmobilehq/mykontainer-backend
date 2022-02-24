from . import views
from django.urls import path


urlpatterns = [
    path('shipping_companies/', views.shipping_company),
    path('shipping_companies/<uuid:company_id>', views.shipping_company_detail),
    path('bay_area/', views.bay_area),
    path('bay_area/<uuid:bay_area_id>', views.bay_area_detail),
]
