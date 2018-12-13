from .views import (
    CountryApiView,
    WorldApiView,
    TopCountriesApiView
)
from django.urls import path
from rest_framework.authtoken import views


urlpatterns = [
    path('country/<int:country_id>', CountryApiView.as_view(), name='country-data-api'),
    path('world', WorldApiView.as_view(), name='world-data-api'),
    path('top_countries', TopCountriesApiView.as_view(), name='top-countries-api')
]
