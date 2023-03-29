from django_filters import rest_framework as filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.emails.models import Email, EmailTemplate

from .filters import EmailFilter
from .serializers import EmailSerializer, EmailTemplateSerializer


class EmailTemplateViewSet(ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def get_permissions(self):
        if self.action in ["post", "put", "patch", "delete"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class EmailViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmailFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
