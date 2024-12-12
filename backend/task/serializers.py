from django.utils import timezone
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['edited_at', 'created_at', 'author', 'visibility']

    is_new = serializers.SerializerMethodField()
    username = serializers.StringRelatedField(source="author")

    def get_is_new(self, obj):
        """Если таска создана не позднее 1 дня - помечаем ее флагом 'is_new = true' """
        return True if (timezone.now() - obj.created_at).days < 1 else False
