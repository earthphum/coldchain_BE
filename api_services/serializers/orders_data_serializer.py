from rest_framework import serializers
from ..models.orders_data import OrdersData

class OrdersDataSerializer(serializers.ModelSerializer):
    class Meta :
        model = OrdersData
        fields = '__all__'