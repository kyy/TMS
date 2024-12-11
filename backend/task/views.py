from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task

class TaskCRUDViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all().order_by('priority').order_by('-status')
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_at=timezone.now())

    @action(detail=True, methods=['get', 'put'])
    def delete(self, request, pk=None):
        """Удаление таски (без удаления из БД)"""
        try:
            task = self.get_object()
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=404)
        if self.request.POST:
            try:
                task.visibility = False
                task.save()
            finally:
                return Response({"visibility": f"{task.visibility}"}, status=200)

        return Response({"message": f"Task '{task.name}'"}, status=200)


