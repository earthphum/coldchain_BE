from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from ..models import CustomersData
from ..serializers import CustomerDataSerializer

class CustomersDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomersData.objects.all()
    serializer_class = CustomerDataSerializer