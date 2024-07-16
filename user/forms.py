from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
