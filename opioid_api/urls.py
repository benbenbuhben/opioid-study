from .views import (
    CountryApiView,
)
from django.urls import path
from rest_framework.authtoken import views


urlpatterns = [
    path('country/<int:country_id>', CountryApiView.as_view(), name='country-data-api')
]
