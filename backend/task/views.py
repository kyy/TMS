from django.utils import timezone
from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Task


class TaskCRUDViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_at=timezone.now())
