from rest_framework import serializers
from ..models.customers_data import CustomersData

class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersData
        fields = '__all__'