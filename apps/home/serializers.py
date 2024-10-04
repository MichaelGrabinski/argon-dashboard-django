from rest_framework import serializers
from apps.home.models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Task
        fields = ('id', 'title', 'start_date', 'due_date', 'hours', 'progress', 'parent_task')
        
        
class ProjectImportSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    manager = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    project_type = serializers.CharField(required=False, allow_blank=True, default='other')
    square_footage = serializers.FloatField(required=False, default=0)
    allotted_budget = serializers.FloatField(required=False, default=0.0)

    def create(self, validated_data):
        manager_username = validated_data.pop('manager', '')
        manager = None
        if manager_username:
            try:
                manager = User.objects.get(username=manager_username)
            except User.DoesNotExist:
                pass  # Handle as needed
        validated_data['manager'] = manager
        project, created = Project.objects.update_or_create(
            title=validated_data['title'],
            defaults=validated_data
        )
        return project