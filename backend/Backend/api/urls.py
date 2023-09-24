# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the viewsets.
router = DefaultRouter()
router.register(r'citizens', views.CitizenViewSet)
router.register(r'drivers', views.DriverViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
