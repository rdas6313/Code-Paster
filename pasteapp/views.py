from rest_framework.viewsets import ModelViewSet
from .models import Paste
from .serializers import PasteSerializer


class PasteViewSet(ModelViewSet):
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer
