from django.contrib.auth.models import User
from dashboard.models import Dashboard

def dashboards_context(request):
    if request.user.is_authenticated:
        user = request.user
        user_groups = user.groups.all()
        user_group_ids = user_groups.values_list('id', flat=True)

        # Obtener dashboards asignados directamente al usuario
        direct_dashboards = Dashboard.objects.filter(permission__user=user)

        # Obtener dashboards asignados a los grupos del usuario
        group_dashboards = Dashboard.objects.filter(permission__group__in=user_group_ids).distinct()

        # Obtener IDs de dashboards que están asignados a grupos
        group_dashboard_ids = group_dashboards.values_list('id', flat=True)

        # Filtrar dashboards directos eliminando los que ya están en group_dashboards
        direct_dashboards = direct_dashboards.exclude(id__in=group_dashboard_ids)

        # Inicializar un diccionario para almacenar los dashboards por grupo
        group_dashboards_by_group = {group: [] for group in user_groups}

        # Asignar dashboards a cada grupo
        for dashboard in group_dashboards:
            # Obtener los grupos asociados a este dashboard
            groups = dashboard.permission.group_set.filter(id__in=user_group_ids).order_by('id')
            for group in groups:
                group_dashboards_by_group[group].append(dashboard)
                break

        # Eliminar grupos que no contienen dashboards
        group_dashboards_by_group = {group: dashboards for group, dashboards in group_dashboards_by_group.items() if dashboards}

        return {
            'direct_dashboards': direct_dashboards,
            'group_dashboards_by_group': group_dashboards_by_group
        }
    
    return {}