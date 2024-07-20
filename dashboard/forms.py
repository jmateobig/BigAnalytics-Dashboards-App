# forms.py
from django import forms
from django.contrib.auth.models import Group
from .models import Dashboard
from django_select2 import forms as s2forms

class CustomSelect2Multiple(s2forms.Select2MultipleWidget):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-select2'}  # Puedes personalizar las clases de estilo aquí
        super().__init__(*args, **kwargs)

class DashboardCreateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,
        label='Grupos a asignar'
    )

    class Meta:
        model = Dashboard
        fields = ['name', 'title', 'description', 'url', 'groups']
        labels = {
            'name': 'Nombre',
            'title': 'Título',
            'description': 'Descripción',
            'url': 'URL',
        }