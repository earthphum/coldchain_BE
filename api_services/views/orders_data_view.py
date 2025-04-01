from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from ..models import OrdersData
from ..serializers import OrdersDataSerializer
from rest_framework.response import Response
from ..services.create_customer import get_or_create_customer

class OrdersDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrdersData.objects.all()
    serializer_class = OrdersDataSerializer

    def create(self, request, *args, **kwargs):
        customer_name = request.data.get('customer_name')
        address = request.data.get('address')
        
        if not customer_name:
            return Response({"error": "customer_name is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not address:
            return Response({"error": "address is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Use service function to handle customer creation/updating
        customer = get_or_create_customer(customer_name, address)
        
        order_data = request.data.copy()  
        order_data['customer'] = customer.id  
        order_serializer = self.get_serializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
