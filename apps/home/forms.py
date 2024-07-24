from django import forms
from .models import Tool

class ToolSearchForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name']
