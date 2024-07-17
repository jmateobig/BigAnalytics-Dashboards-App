from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
    
# @method_decorator(csrf_exempt, name='dispatch')
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
        filtered_users = users.filter(username__icontains=search_value)

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
            'data': list(paginated_users.values('id', 'username', 'email', 'is_active')),
        }

        return JsonResponse(data)