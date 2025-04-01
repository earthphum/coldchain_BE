from rest_framework import serializers
from api_services.models import SensorData  

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__' 
