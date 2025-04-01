from rest_framework import serializers
from ..models import OriginData

class OriginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginData
        fields = '__all__'
