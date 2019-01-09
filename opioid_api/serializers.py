from rest_framework import serializers
from opioid_api.models import Opioids


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opioids
        fields = ('year', 'location_id', 'location_name', 'sex_id', 'sex_name', 'val', 'upper', 'lower', 'rank', 'sex_percentage', 'percent_change', 'average_percent_change', 'raw_decrease_from_peak',
        'raw_increase_from_min',  'avg_percent_change_since_peak', 'avg_percent_change_since_min', 'peak', 'min')

