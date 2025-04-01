from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from ..models import SensorData 
from ..serializers import SensorDataSerializer

class DeviceSensorDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

