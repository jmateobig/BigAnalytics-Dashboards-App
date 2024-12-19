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

        # Inicializar un diccionario para almacenar los dashboards agrupados por categoría y grupo
        dashboards_by_category = {}

        # Recorrer los grupos del usuario
        for group in user_groups:
            # Obtener la categoría asociada al grupo (si existe)
            category = getattr(group, 'category', None)

            if category:  # Solo agrupar si el grupo tiene una categoría
                # Asegurarse de que la categoría esté en el diccionario
                if category not in dashboards_by_category:
                    dashboards_by_category[category] = {}

                # Obtener los dashboards asociados al grupo
                dashboards = group_dashboards.filter(permission__group=group).distinct()

                # Agregar el grupo y sus dashboards a la categoría correspondiente
                dashboards_by_category[category][group] = dashboards

        # Eliminar categorías que no contienen ningún grupo con dashboards
        dashboards_by_category = {
            category: groups for category, groups in dashboards_by_category.items() if groups
        }

        return {
            'direct_dashboards': direct_dashboards,
            'dashboards_by_category': dashboards_by_category
        }

    return {}