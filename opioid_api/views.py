from django.shortcuts import render
from rest_framework import generics
from opioid_api.models import Opioids
from opioid_api.serializers import (
    CountrySerializer,
)


class CountryApiView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Opioids.objects.filter(
            location_id=self.kwargs['country_id']).filter(sex_id=3).order_by('year')
