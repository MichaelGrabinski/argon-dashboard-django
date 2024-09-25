from django import forms
from django.contrib.auth.models import User 
from .models import (
    Tool, Tag, Task, Comment, Attachment, Unit, Material,
    LaborEntry, ProjectNote, ProjectAttachment, ReferenceMaterial,
    Project, ProjectImage
)

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
            'priority': forms.Select(),
            'category': forms.TextInput(attrs={'value': 'General'}),
            'hours': forms.NumberInput(attrs={'value': 1}),
            'assigned_to': forms.Select(),
            'location': forms.Select(),  # Use a dropdown for location
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        fields = ['project', 'type', 'content']

class ImportConversationForm(forms.Form):
    conversations_file = forms.FileField(
        label='Select a JSON file to import',
        help_text='Max. 5 megabytes'
    )

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

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['category', 'description', 'unit_cost', 'quantity']

class LaborEntryForm(forms.ModelForm):
    class Meta:
        model = LaborEntry
        fields = ['user', 'hours_worked', 'pay_rate', 'date']

class ProjectNoteForm(forms.ModelForm):
    class Meta:
        model = ProjectNote
        fields = ['content']

class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = ['file']