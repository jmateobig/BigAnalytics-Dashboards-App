# forms.py
from django import forms
from django.contrib.auth.models import Group, User
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

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,
        label='Usuarios a asignar'
    )

    class Meta:
        model = Dashboard
        fields = ['name', 'title', 'description', 'url', 'groups', 'users']
        labels = {
            'name': 'Nombre',
            'title': 'Título',
            'description': 'Descripción',
            'url': 'URL',
        }

class DashboardEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,  # Puedes usar un widget personalizado si lo tienes
        label='Grupos'
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,  # Puedes usar un widget personalizado si lo tienes
        label='Usuarios'
    )

    class Meta:
        model = Dashboard
        fields = ['name', 'title', 'description', 'url']
        labels = {
            'name': 'Nombre',
            'title': 'Título',
            'description': 'Descripción',
            'url': 'URL',
        }