from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..serializers.route_planner_serializer import RoutePlannerSerializer
from ..services.route_planner_service import plan_routes

class RoutePlannerView(APIView):
    """
    API view for planning delivery routes.
    
    Expects a POST request with 'num_riders', 'delivery_date', and 'rider_names'.
    Returns delivery details, customer coordinates, clustering results, and assigned routes.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoutePlannerSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        num_riders = serializer.validated_data.get("num_riders")
        # Format delivery_date to YYYY-MM-DD string
        delivery_date = serializer.validated_data.get("delivery_date").strftime("%Y-%m-%d")
        rider_names = serializer.validated_data.get("rider_names", [])

        try:
            result = plan_routes(num_riders, delivery_date, rider_names)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log unexpected errors here if needed
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status=status.HTTP_200_OK)
