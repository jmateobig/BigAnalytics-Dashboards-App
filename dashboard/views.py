from django.views.generic import  ListView, View, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission

from notification.services import send_notification_to_users_and_groups
from .models import Dashboard
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from .forms import DashboardCreateForm, DashboardEditForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class DashboardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Dashboard
    template_name = 'dashboard_list.html'
    context_object_name = 'dashboards'
    permission_required = 'dashboard.add_dashboard'


class DashboardListJsonView(View):
    def post(self, request, *args, **kwargs):
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column = request.POST.get('order[0][column]', 0)
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Obtener datos filtrados y ordenados
        dashboards = Dashboard.objects.all()
        filtered_dashboards = dashboards.filter(name__icontains=search_value)
        filtered_dashboards = dashboards.filter(Q(name__icontains=search_value) | Q(title__icontains=search_value) | Q(description__icontains=search_value))

        if order_dir == 'asc':
            order_column_name = request.POST.get(f'columns[{order_column}][data]', 'id')
        else:
            order_column_name = '-' + request.POST.get(f'columns[{order_column}][data]', 'id')

        ordered_dashboards = filtered_dashboards.order_by(order_column_name)
        total_records = filtered_dashboards.count()

        paginated_dashboards = ordered_dashboards[start:start + length]

        # Calcular el número de usuarios que tienen el permiso del dashboard
        data = []
        for dashboard in paginated_dashboards:
            users_with_permission = User.objects.filter(
                Q(user_permissions=dashboard.permission) |
                Q(groups__permissions=dashboard.permission)
            ).distinct().count()

            data.append({
                'id': dashboard.id,
                'name': dashboard.name,
                'title': dashboard.title,
                'description': dashboard.description,
                'url': dashboard.url,
                'num_users': users_with_permission
            })

        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data,
        }

        return JsonResponse(response)
    

class DashboardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Dashboard
    form_class = DashboardCreateForm
    template_name = 'dashboard_create.html'
    permission_required = 'dashboard.add_dashboard'
    success_url = reverse_lazy('dashboard:list')

    def form_valid(self, form):
        # Crear el Dashboard
        dashboard = form.save(commit=False)
        dashboard.save()

        # Obtener el ContentType
        content_type = ContentType.objects.get(app_label='render', model='dashboard')

        # Crear el permiso
        permission_name = f'Can read {dashboard.name}'
        permission_codename = dashboard.name.replace(' ', '_').lower()
        permission = Permission.objects.create(
            name=permission_name,
            codename=permission_codename,
            content_type=content_type
        )

        # Asignar el permiso al Dashboard
        dashboard.permission = permission
        dashboard.save()

        # Asignar el permiso a los grupos seleccionados
        groups = form.cleaned_data['groups']
        for group in groups:
            group.permissions.add(permission)

        # Asignar el permiso a los usuarios seleccionados
        users = form.cleaned_data['users']
        for user in users:
            user.user_permissions.add(permission)

        if users or groups:
            send_notification_to_users_and_groups(
                title="Acceso al Nuevo Dashboard",
                description=f"Se te ha otorgado acceso al nuevo Dashboard '{dashboard.name}'.",
                url=reverse_lazy('dashboard:render', args=[dashboard.id]),
                user_list=users,
                group_list=groups
            )


        return super().form_valid(form)
    

class DashboardDetailJsonView(View):
    def post(self, request, *args, **kwargs):
        dashboard_id = request.POST.get('dashboard_id')
        try:
            dashboard = Dashboard.objects.get(pk=dashboard_id)

            # Obtener grupos y usuarios con el permiso
            groups_with_permission = Group.objects.filter(permissions=dashboard.permission)
            users_with_permission = User.objects.filter(user_permissions=dashboard.permission).distinct()
            
            # Obtener usuarios indirectos a través de grupos
            indirect_users = User.objects.filter(groups__in=groups_with_permission).distinct()
            
            # Crear un diccionario para almacenar usuarios con sus banderas
            users_data = {}

            for user in indirect_users:
                if user.username not in users_data:
                    users_data[user.username] = {
                        'full_name': f"{user.get_full_name()} ({user.username})",
                        'flag': 'warning'
                    }

            for user in users_with_permission:
                users_data[user.username] = {
                    'full_name': f"{user.get_full_name()} ({user.username})",
                    'flag': 'success'
                }
            
            # Convertir el diccionario en una lista y ordenar
            users_list = [{'full_name': user_data['full_name'], 'flag': user_data['flag']} 
                          for username, user_data in users_data.items()]
            users_list.sort(key=lambda x: (x['flag'] == 'warning', x['full_name']))

            data = {
                'id': dashboard.id,
                'name': dashboard.name,
                'title': dashboard.title,
                'description': dashboard.description,
                'url': dashboard.url,
                'groups': list(groups_with_permission.values_list('name', flat=True)),
                'users': users_list,
            }

            return JsonResponse({'status': 'success', 'data': data})
        except Dashboard.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Dashboard not found'}, status=404)
        

class DashboardEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'dashboard_edit.html'
    permission_required = 'dashboard.change_dashboard'
    success_url = reverse_lazy('dashboard:list')

    def get(self, request, dashboard_id, *args, **kwargs):
        dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
        form = DashboardEditForm(instance=dashboard)
        form.fields['groups'].initial = Group.objects.filter(permissions=dashboard.permission)
        form.fields['users'].initial = User.objects.filter(user_permissions=dashboard.permission)
        return render(request, self.template_name, {'form': form, 'dashboard': dashboard})

    def post(self, request, dashboard_id, *args, **kwargs):
        dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
        form = DashboardEditForm(request.POST, instance=dashboard)
        if form.is_valid():
            
            # Obtener permisos antiguos del dashboard
            old_groups_ids = set(Group.objects.filter(permissions=dashboard.permission).values_list('id', flat=True))
            old_users_ids = set(User.objects.filter(user_permissions=dashboard.permission).values_list('id', flat=True))
            old_groups = Group.objects.filter(id__in=old_groups_ids)
            old_users = User.objects.filter(id__in=old_users_ids)

            # Guardar los cambios del formulario
            dashboard = form.save()

            # Update groups and users with the permission
            groups = form.cleaned_data['groups']
            users = form.cleaned_data['users']

            # Actualizar grupos y usuarios con el permiso
            dashboard.permission.group_set.set(groups)
            dashboard.permission.user_set.set(users)

            # Calcular grupos y usuarios añadidos y eliminados
            new_groups = set(groups)
            new_users = set(users)

            added_groups = new_groups - set(old_groups)
            removed_groups = set(old_groups) - new_groups

            added_users = new_users - set(old_users)
            removed_users = set(old_users) - new_users

            if removed_users or removed_groups:
                send_notification_to_users_and_groups(
                    title="Acceso al Dashboard Revocado",
                    description=f"Se te ha retirado el acceso al Dashboard '{dashboard.name}'.",
                    url=reverse_lazy('notification:list'),
                    user_list=list(removed_users),
                    group_list=list(removed_groups)
                )

            if added_groups or added_users:
                send_notification_to_users_and_groups(
                    title="Acceso al Dashboard Concedido",
                    description=f"Se te ha otorgado acceso al Dashboard '{dashboard.name}'.",
                    url=reverse_lazy('dashboard:render', args=[dashboard_id]),
                    user_list=list(added_users),
                    group_list=list(added_groups)
                )

            messages.success(request, '¡Dashboard actualizado con éxito!')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'dashboard': dashboard})
    

class DashboardDeleteView(View):
    def post(self, request, *args, **kwargs):
        dashboard_id = request.POST.get('dashboard_id')
        try:
            dashboard = get_object_or_404(Dashboard, pk=dashboard_id)
            permission = dashboard.permission

            # Eliminar asignaciones de permiso a grupos
            groups_with_permission = Group.objects.filter(permissions=permission)
            for group in groups_with_permission:
                group.permissions.remove(permission)

            # Eliminar asignaciones de permiso a usuarios
            users_with_permission = User.objects.filter(user_permissions=permission)
            for user in users_with_permission:
                user.user_permissions.remove(permission)

            # Eliminar el dashboard
            dashboard.delete()

            # Eliminar el permiso
            if permission:
                permission.delete()

            return JsonResponse({'status': 'success', 'message': 'Dashboard eliminado con éxito'})
        except Dashboard.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Dashboard no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

class DashboardRenderView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_render.html'

    def has_permission(self, permission, user):
        admin_group = Group.objects.filter(name='Admin').first()
        if admin_group and admin_group in user.groups.all():
            return True
        direct_permission_codenames = set(user.user_permissions.values_list('codename', flat=True))
        group_permission_codenames = set(Permission.objects.filter(group__user=user).values_list('codename', flat=True))
        combined_codenames = direct_permission_codenames.union(group_permission_codenames)
        return permission.codename in combined_codenames
    

    def get(self, request, *args, **kwargs):
        dashboard_id = self.kwargs.get('dashboard_id')
        dashboard = get_object_or_404(Dashboard, id=dashboard_id)

        # Obtener el permiso asociado al dashboard
        permission = dashboard.permission

        if not self.has_permission(permission, request.user):
            raise PermissionDenied
        
        context = {
            'dashboard': dashboard
        }
        return self.render_to_response(context)