from rest_framework_jwt.views import obtain_jwt_token

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/v1/', include('offers.api.urls')),
    path(r'api/v1/auth/', include('rest_framework.urls')),
]
