from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'