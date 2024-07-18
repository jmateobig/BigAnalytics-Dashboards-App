from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Value, Q
from django.db.models.functions import Concat
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import UserCreateForm, UserEditForm
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    permission_required = 'publicacion.add_user'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('user:list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_unusable_password()
        user.save()
        form.save_m2m()  # Guardar los grupos asociados

        # Obtener el dominio actual
        current_site = get_current_site(self.request)
        domain = current_site.domain


        # Enviar correo de bienvenida
        subject = 'Bienvenido a Nuestro Servicio'
        html_message = render_to_string('email/welcome_email.html', {'user': user, 'domain': domain })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = user.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return super().form_valid(form)


class UserEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'user_edit.html'
    permission_required = 'publicacion.add_user'

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        form = UserEditForm(instance=user)
        groups = Group.objects.all()
        return render(request, self.template_name, {'form': form, 'user': user, 'groups': groups})

    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Update user groups
            group_ids = request.POST.getlist('groups')
            user.groups.set(group_ids)
            user.save()
            return redirect('user:list')  # Redirigir a la lista de usuarios después de guardar los cambios
        groups = Group.objects.all()
        return render(request, self.template_name, {'form': form, 'user': user, 'groups': groups})
    

class UserListJsonView(View):
    def post(self, request, *args, **kwargs):
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column = request.POST.get('order[0][column]', 0)
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Obtener datos filtrados y ordenados
        users = User.objects.all()
        filtered_users = users.filter(Q(username__icontains=search_value) | Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) | Q(email__icontains=search_value))

        if order_dir == 'asc':
            order_column_name = request.POST.get(f'columns[{order_column}][data]', 'id')
        else:
            order_column_name = '-' + request.POST.get(f'columns[{order_column}][data]', 'id')

        ordered_users = filtered_users.order_by(order_column_name)
        total_records = filtered_users.count()

        paginated_users = ordered_users[start:start + length]

        data = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': list(paginated_users.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).values('id', 'full_name', 'username', 'email', 'is_active')),
        }

        return JsonResponse(data)
    

class UserDetailJsonView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            data = {
                'id': user.id,
                'full_name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'is_active': user.is_active,
                'groups': list(user.groups.values_list('name', flat=True)),
            }
            return JsonResponse({'status': 'success', 'data': data})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        

class UserToggleStatusView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({'status': 'success', 'is_active': user.is_active})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            print("hola")
            user.groups.clear()
            user.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Usuario Eliminado'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


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