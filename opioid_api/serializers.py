from rest_framework import serializers
from opioid_api.models import Opioids


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opioids
        fields = ('year', 'location_id', 'location_name', 'sex_id', 'sex_name', 'val', 'upper', 'lower', 'rank')
