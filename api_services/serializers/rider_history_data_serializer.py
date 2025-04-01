from rest_framework import serializers
from ..models import RiderHistoryData

class RiderHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderHistoryData
        fields = '__all__'
