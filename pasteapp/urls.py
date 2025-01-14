from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework import routers
from .views import PasteViewSet

router = routers.SimpleRouter()
router.register(r'paste', PasteViewSet, basename='paste')

urlpatterns = router.urls
