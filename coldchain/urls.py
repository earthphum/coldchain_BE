from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenObtainPairView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_services.urls')),
    path('api/login/token/',TokenObtainPairView.as_view(),name= 'token_obtain_pair'),
    path('api/login/token/refresh/',TokenRefreshView.as_view(),name= 'token_refresh'),
    path('api/login/token/logout',TokenBlacklistView.as_view(),name= 'token_blacklist'),
    # path('api/test/',DeviceSensorDataView.as_view(),name='protect'),
    

]
