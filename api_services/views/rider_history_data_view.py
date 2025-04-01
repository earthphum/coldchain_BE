from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from ..models import RiderHistoryData
from ..serializers import RiderHistoryDataSerializer

class RiderHistoryDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RiderHistoryData.objects.all()
    serializer_class = RiderHistoryDataSerializer