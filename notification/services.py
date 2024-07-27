# notifications/services.py

from django.contrib.auth.models import User, Group
from .models import Notification

def send_notification_to_users_and_groups(title, description, url, user_list=None, group_list=None):
    if user_list is None:
        user_list = []
    if group_list is None:
        group_list = []

    # Obtener todos los usuarios de los grupos proporcionados
    group_users = User.objects.filter(groups__in=group_list).distinct()

    # Combinar los usuarios proporcionados con los usuarios de los grupos
    all_users = set(user_list).union(set(group_users))

    # Enviar la notificación a todos los usuarios únicos
    for user in all_users:
        print(user)
        notificacion=Notification.objects.create(
            title=title,
            description=description,
            url=url,
            user=user,
            seen=False
        )
        notificacion.save()
