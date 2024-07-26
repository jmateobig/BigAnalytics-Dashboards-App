from django.contrib.auth.models import User
from dashboard.models import Dashboard

def dashboards_context(request):
    if request.user.is_authenticated:
        user = request.user
        # Dashboards asignados directamente
        direct_dashboards = Dashboard.objects.filter(permission__user=user)
        
        # Dashboards asignados por grupo
        group_dashboards = Dashboard.objects.filter(permission__group__user=user).distinct()
        
        # Agrupar dashboards por grupo
        group_dashboards_by_group = {}
        for dashboard in group_dashboards:
            groups = dashboard.permission.group_set.all()
            for group in groups:
                if group not in group_dashboards_by_group:
                    group_dashboards_by_group[group] = []
                group_dashboards_by_group[group].append(dashboard)

        # Filtrar dashboards directos eliminando los que ya están en group_dashboards
        direct_dashboards = direct_dashboards.exclude(id__in=group_dashboards.values_list('id', flat=True))

        return {
            'direct_dashboards': direct_dashboards,
            'group_dashboards_by_group': group_dashboards_by_group
        }
    return {}
