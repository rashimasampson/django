from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('wall_app.urls')),
]
