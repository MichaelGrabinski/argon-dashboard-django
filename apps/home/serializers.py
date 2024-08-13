from rest_framework import serializers
from apps.home.models import Task

class TaskSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Task
        fields = ('id', 'title', 'start_date', 'due_date', 'hours', 'progress', 'parent_task')