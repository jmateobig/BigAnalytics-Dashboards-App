from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import  ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from .forms import GroupCreateForm, GroupEditForm
from notification.services import send_notification_to_users_and_groups


class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'group'
    permission_required = 'publicacion.add_group'


class GroupListJsonView(View):
    def post(self, request, *args, **kwargs):
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column = request.POST.get('order[0][column]', 0)
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Obtener datos filtrados y ordenados
        groups = Group.objects.all()
        filtered_groups = groups.filter(name__icontains=search_value)

        if order_dir == 'asc':
            order_column_name = request.POST.get(f'columns[{order_column}][data]', 'id')
        else:
            order_column_name = '-' + request.POST.get(f'columns[{order_column}][data]', 'id')

        ordered_groups = filtered_groups.order_by(order_column_name)
        total_records = filtered_groups.count()

        paginated_groups = ordered_groups[start:start + length]

        data = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': list(
                paginated_groups.annotate(num_users=Count('user')).values('id', 'name', 'num_users')
            ),
        }

        return JsonResponse(data)
    

class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'group_create.html'
    permission_required = 'publicacion.add_group'
    success_url = reverse_lazy('group:list')  

    def form_valid(self, form):
        group = form.save()
        users = form.cleaned_data['users']
        group.user_set.set(users)
        send_group_notification(users=users, title="Añadido a un nuevo grupo",  description=f"Has sido añadido al grupo: {group.name}.")
        messages.success(self.request, 'Grupo creado exitosamente')
        return super().form_valid(form)


class GroupDetailJsonView(View):
    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(pk=group_id)
            users = User.objects.filter(groups=group)
            data = {
                'id': group.id,
                'name': group.name,
                'users': list(users.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).values('username', 'full_name', 'is_active')),
            }
            return JsonResponse({'status': 'success', 'data': data})
        except Group.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Group not found'}, status=404)
        

class GroupEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'group_edit.html'
    permission_required = 'publicacion.change_group'
    success_url = reverse_lazy('group:list')

    def get(self, request, group_id, *args, **kwargs):
        group = get_object_or_404(Group, pk=group_id)
        form = GroupEditForm(instance=group)
        form.fields['users'].initial = group.user_set.all()  # Inicializa el campo de usuarios
        return render(request, self.template_name, {'form': form, 'group': group})

    def post(self, request, group_id, *args, **kwargs):
        group = get_object_or_404(Group, pk=group_id)
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            # Obtener los usuarios actuales del grupo
            old_users = set(group.user_set.all())

            # Guardar los cambios del formulario
            form.save()
            # Update group users
            user_ids = request.POST.getlist('users')
            users = User.objects.filter(id__in=user_ids)
            group.user_set.set(users)
            group.save()

            # Calcular grupos añadidos y eliminados
            updated_users = set(group.user_set.all())
            added_users = updated_users.difference(old_users)
            removed_users = old_users.difference(updated_users)

            send_group_notification(users=added_users,   title="Añadido a un Nuevo Grupo", description=f"Has sido añadido al grupo '{group.name}'.")
            send_group_notification(users=removed_users, title="Eliminación del Grupo",    description=f"Has sido eliminado del grupo '{group.name}'.")

            messages.success(request, '¡Grupo actualizado con éxito!')
            return redirect(self.success_url)  # Redirigir a la lista de grupos después de guardar los cambios
        return render(request, self.template_name, {'form': form, 'group': group})
    

class GroupDeleteView(View):
    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id')
        try:
            if int(group_id) in [1, 2]:
                return JsonResponse({'status': 'error', 'message': 'No se puede eliminar este grupo'}, status=403)
                
            group = Group.objects.get(pk=group_id)
            group.user_set.clear()
            group.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Grupo Eliminado'})
        except Group.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Grupo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

def send_group_notification(users, title, description):
        # Configurar el título y la descripción de la notificación
        notification_url = reverse_lazy('notification:list')  # URL a la que se puede redirigir desde la notificación
        # Enviar la notificación usando el servicio
        send_notification_to_users_and_groups(
            user_list=users, group_list=[], title=title, description=description, url=notification_url
        )