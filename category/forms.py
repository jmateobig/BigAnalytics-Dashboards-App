from django import forms
from django.contrib.auth.models import Group
from .models import Category
from django_select2 import forms as s2forms

class CustomSelect2Multiple(s2forms.Select2MultipleWidget):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-select2'}  # Personalización del widget
        super().__init__(*args, **kwargs)

class CategoryForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,
        label='Grupos asignados'
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'groups']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }

    def save(self, commit=True):
        # Lógica personalizada para manejar la asignación de grupos
        instance = super().save(commit=False)

        if commit:
            instance.save()

        # Obtener los grupos seleccionados del formulario
        selected_groups = self.cleaned_data.get('groups', [])

        # Reasignar grupos seleccionados a la categoría actual
        Group.objects.filter(category=instance).exclude(pk__in=[group.pk for group in selected_groups]).update(category=None)
        selected_groups.update(category=instance)

        return instance
