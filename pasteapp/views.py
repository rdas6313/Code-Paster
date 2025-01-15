from rest_framework.viewsets import ModelViewSet
from .models import Paste
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import PastePermission
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PasteViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action in ['me', 'password']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [PastePermission]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve_password_view':
            return SinglePastePasswordSerializer
        return PasteSerializer

    def get_queryset(self):
        queryset = Paste.objects.all()
        if self.action == 'list':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    (Q(sharable=True) & Q(password='')) | Q(user=self.request.user))
            else:
                queryset = queryset.filter(
                    sharable=True, password='')
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

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def password(self, request, pk=None):
        paste = self.get_object()
        paste.password = ''
        paste.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def retrieve_password_view(self, request, pk=None):
        serializer = SinglePastePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password', None)
        paste = self.get_object()
        if paste.is_valid_password(password):
            serializer = PasteSerializer(paste)
            return Response(serializer.data)
        else:
            raise PermissionDenied(
                detail='Authentication creadential is not valid', code='invalid_password')
