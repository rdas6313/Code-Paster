from rest_framework.viewsets import ModelViewSet
from .models import Paste
from .serializers import PasteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import PastePermission
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PasteViewSet(ModelViewSet):

    serializer_class = PasteSerializer
    permission_classes = [PastePermission]

    def get_queryset(self):
        queryset = Paste.objects.all()
        if self.action == 'list':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    Q(sharable=True) | Q(user=self.request.user))
            else:
                queryset = queryset.filter(sharable=True)
        return queryset

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {'user': self.request.user}
        return super().get_serializer_context()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = PasteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
