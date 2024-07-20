from django.views.generic import  ListView, View, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from .models import Dashboard
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .forms import DashboardCreateForm
from .models import Dashboard
from django.urls import reverse_lazy


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
    success_url = reverse_lazy('dashboard:list')
    permission_required = 'dashboard.add_dashboard'

    def form_valid(self, form):
        # Crear el Dashboard
        dashboard = form.save(commit=False)
        dashboard.save()

        # Crear el ContentType
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

        return super().form_valid(form)