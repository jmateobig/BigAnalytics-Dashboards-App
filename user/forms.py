from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User, Group

class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'form-check-input'  # Agregar clase de Bootstrap para los checkboxes
        return super().render(name, value, attrs, renderer)

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
        widget=CheckboxSelectMultiple,  # Usar el widget de checkboxes personalizado
        label='Grupos'
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'last_name', 'email', 'groups']
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
        widget=CheckboxSelectMultiple,  # Usar el widget de checkboxes personalizado
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
