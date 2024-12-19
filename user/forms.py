from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User, Group
from django_select2 import forms as s2forms
from category.models import Category
    
class CustomSelect2Multiple(s2forms.Select2MultipleWidget):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-select2'}  # Puedes personalizar las clases de estilo aquí
        super().__init__(*args, **kwargs)


class CustomSelect2(s2forms.Select2Widget):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-select2'}  # Personaliza las clases de estilo aquí
        super().__init__(*args, **kwargs)


class CustomLoginForm(LoginForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Login'))


class CustomSignupForm(SignupForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('signup', 'Sign Up'))


class UserCreateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,  # Usar el widget de checkboxes personalizado
        label='Grupos'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'groups']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Usuario',
            'email': 'Correo Electrónico',
        }


class UserEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,  # Usar el widget de checkboxes personalizado
        label='Grupos'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
        }


class GroupCreateForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,
        label='Usuarios'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=CustomSelect2,
        label='Categoría',
        empty_label="Seleccione una categoría"
    )

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = self.user_label_from_instance

    @staticmethod
    def user_label_from_instance(user):
        return f"{user.first_name} ({user.email})"

    class Meta:
        model = Group
        fields = ['name', 'users', 'category']
        labels = {
            'name': 'Nombre del Grupo',
        }


class GroupEditForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=CustomSelect2Multiple,  # Usar el widget de checkboxes
        label='Usuarios'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=CustomSelect2,
        label='Categoría',
        empty_label="Seleccione una categoría"
    )

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = self.user_label_from_instance

        # Si es una instancia de edición, configurar la categoría seleccionada
        if self.instance and self.instance.category:
            self.fields['category'].initial = self.instance.category

    @staticmethod
    def user_label_from_instance(user):
        return f"{user.first_name} ({user.email})"

    class Meta:
        model = Group
        fields = ['name', 'users', 'category']
        labels = {
            'name': 'Nombre del Grupo',
        }