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
            location_id=self.kwargs['country_id']).order_by('year')


class WorldApiView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Opioids.objects.filter(
            location_id=0).order_by('year')


class TopCountriesApiView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        top_countries_qs = Opioids.objects.filter(
            sex_id=3).filter(year=2017).order_by('-val')[:25]

        top_countries_list = [country['location_name'] for country in top_countries_qs.values('location_name')]

        return Opioids.objects.filter(location_name__in=top_countries_list).filter(year=2017)[:75]

