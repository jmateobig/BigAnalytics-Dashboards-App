# forms.py
from django import forms
from django.contrib.auth.models import Group
from .models import Category
from django_select2 import forms as s2forms

class CustomSelect2Multiple(s2forms.Select2MultipleWidget):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-select2'}  # Personalización del widget
        super().__init__(*args, **kwargs)

class CategoryCreateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,
        label='Grupos a asignar'
    )

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = ['name', 'description', 'groups']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }

    def save(self, commit=True):
        # Lógica personalizada para manejar la asignación de grupos
        instance = super(CategoryCreateForm, self).save(commit=False)
        
        # Guardar la categoría primero (si commit=True)
        if commit:
            instance.save()

        # Reasignar grupos seleccionados a la categoría actual
        selected_groups = self.cleaned_data.get('groups', [])
        if selected_groups:
            # Quitar la categoría actual de otros grupos que estaban asignados previamente
            Group.objects.filter(category=instance).exclude(pk__in=[group.pk for group in selected_groups]).update(category=None)
            
            # Asignar la categoría actual a los grupos seleccionados
            selected_groups.update(category=instance)
        
        return instance


class CategoryEditForm(forms.ModelForm):
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
        # Lógica personalizada para manejar la reasignación de grupos
        instance = super(CategoryEditForm, self).save(commit=False)

        if commit:
            instance.save()

        # Obtener los grupos seleccionados del formulario
        selected_groups = self.cleaned_data.get('groups', [])

        # Reasignar grupos seleccionados a la categoría actual
        if selected_groups:
            # Quitar la categoría actual de grupos que ya no están seleccionados
            Group.objects.filter(category=instance).exclude(pk__in=[group.pk for group in selected_groups]).update(category=None)

            # Asignar la categoría actual a los grupos seleccionados
            selected_groups.update(category=instance)

        return instance