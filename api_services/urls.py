from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceSensorDataView , CustomersDataView , OrdersDataView , OriginDataView ,RiderHistoryDataView,RoutePlannerView


router = DefaultRouter()
router.register(r'device-sensor', DeviceSensorDataView, basename='device-sensor')
router.register(r'orders',OrdersDataView,basename='orders')
router.register(r'customers',CustomersDataView,basename='customers')
router.register(r'rider-history',RiderHistoryDataView,basename='rider-history')


urlpatterns = [
    path('', include(router.urls)),  # ViewSet endpoints
    path('origin/',OriginDataView.as_view(),name='origin'),
    path('route-planner/',RoutePlannerView.as_view(),name="route-planner")
]