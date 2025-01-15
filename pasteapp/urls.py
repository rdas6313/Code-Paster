from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import PasteViewSet

router = routers.SimpleRouter()
router.register(r'paste', PasteViewSet, basename='paste')


urlpatterns = [
    path('paste/me/', PasteViewSet.as_view({'get': 'me'})),
    path('paste/<str:pk>/', PasteViewSet.as_view(
         {
             'post': 'retrieve_password_view',
             'get': 'retrieve',
             'patch': 'partial_update',
             'put': 'update',
             'delete': 'destroy'
         }), name='paste-retrieve-password'),
    path("", include(router.urls)),

]
