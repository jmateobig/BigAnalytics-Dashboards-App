from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'user_list.html'


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    permission_required = 'publicacion.add_user'


class UserCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'user_create.html'


class UserEditView(LoginRequiredMixin, TemplateView):
    template_name = 'user_edit.html'


class UserDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_details.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups = user.groups.all()
        context = {'user': user, 'groups': groups}
        return context


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        messages.success(request, '¡Perfil actualizado con éxito!')
        return redirect('user:profile')
