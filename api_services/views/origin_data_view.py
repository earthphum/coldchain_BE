from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import OriginData
from ..serializers import OriginDataSerializer
from rest_framework.permissions import IsAuthenticated
class OriginDataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        origin = OriginData.objects.first()
        if origin:
            serializer = OriginDataSerializer(origin)
            return Response(serializer.data)
        return Response({"detail": "OriginData not found."}, status=404)

    def post(self, request):
        if OriginData.objects.exists():
            return Response({"error": "OriginData already exists. Use PUT or PATCH to update."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = OriginDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        origin = OriginData.objects.first()
        if not origin:
            return Response({"detail": "OriginData not found."}, status=404)
        serializer = OriginDataSerializer(origin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        origin = OriginData.objects.first()
        if not origin:
            return Response({"detail": "OriginData not found."}, status=404)
        serializer = OriginDataSerializer(origin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
