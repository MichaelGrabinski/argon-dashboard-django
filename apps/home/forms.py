from django import forms
from .models import Tool
from .models import Tag
from .models import Task, Comment, Attachment, Unit 
from django.contrib.auth.models import User 
from .models import ReferenceMaterial

class ToolSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search')
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label='Tag')
    
class TaskForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=True, label="Unit")

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'priority', 'unit']

    def save(self, commit=True):
        task = super().save(commit=False)
        task.location = self.cleaned_data['unit'].location  # Set the location based on the selected unit
        if commit:
            task.save()
        return task
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

class AssignTaskForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Assign to')

class QuickTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'category', 'hours', 'assigned_to', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'value': 'New Task'}),
            'description': forms.Textarea(attrs={'value': 'Description of the task'}),
            'priority': forms.Select(attrs={'value': 'medium'}),
            'category': forms.TextInput(attrs={'value': 'General'}),
            'hours': forms.NumberInput(attrs={'value': 1}),
            'assigned_to': forms.Select(attrs={'value': None}),
            'location': forms.Select(),  # Use a dropdown for location
        }
class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        fields = ['project', 'type', 'content']
        widgets = {
            'type': forms.Select(choices=ReferenceMaterial.PROJECT_REFERENCE_TYPE_CHOICES),
        }