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
        fields = [
            'title', 'description', 'priority', 'category', 'hours', 
            'assigned_to', 'location', 'due_date', 'project', 'phase', 
            'parent_task', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'value': 'New Task'}),
            'description': forms.Textarea(attrs={'value': 'Description of the task'}),
            'priority': forms.Select(attrs={'value': 'medium'}),
            'category': forms.TextInput(attrs={'value': 'General'}),
            'hours': forms.NumberInput(attrs={'value': 1}),
            'assigned_to': forms.Select(attrs={'value': None}),
            'location': forms.Select(),  # Use a dropdown for location
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        
class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        fields = ['project', 'type', 'content']
        widgets = {
            'type': forms.Select(choices=ReferenceMaterial.PROJECT_REFERENCE_TYPE_CHOICES),
        }
        
class ImportConversationForm(forms.Form):
    conversations_file = forms.FileField(
        label='Select a JSON file to import',
        help_text='Max. 5 megabytes'
      )
      
from django import forms
from .models import Project

class StatementUploadForm(forms.Form):
    project_id = forms.ModelChoiceField(queryset=Project.objects.all())
    statement_file = forms.FileField(label='Select PDF Bank Statement')
    
class BankStatementUploadForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    bank_statement_file = forms.FileField(label='Bank Statement (PDF)')

    def clean_bank_statement_file(self):
        file = self.cleaned_data['bank_statement_file']
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError('Please upload a PDF file.')
        return file