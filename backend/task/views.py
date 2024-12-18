from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .ex.permissions import IsAuthor
from .serializers import TaskSerializer
from .models import Task


class TaskCRUDViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('priority').order_by('-status')
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthor, IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, created_at=timezone.now())

    def perform_update(self, serializer):
        serializer.save(edited_at=timezone.now())


