from rest_framework import serializers
class RoutePlannerSerializer(serializers.Serializer):
    num_riders = serializers.IntegerField(min_value=1, max_value=5)
    delivery_date = serializers.DateField()
    rider_names = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        help_text="List of rider names (must match num_riders)"
    )