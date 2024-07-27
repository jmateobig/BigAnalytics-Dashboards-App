from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations


def create_initial_data(apps, schema_editor):
    # Crea el contenido para tu aplicación
    content_type = ContentType.objects.create(app_label='notification',model='notification')
    
    # Crea los permisos para el modelo Notification
    permission_add = Permission.objects.create      (codename=  'add_notification',     name='Can add notification',    content_type=content_type)
    permission_change = Permission.objects.create   (codename=  'change_notification',  name='Can change notification', content_type=content_type)
    permission_delete = Permission.objects.create   (codename=  'delete_notification',  name='Can delete notification', content_type=content_type)
    permission_view = Permission.objects.create     (codename=  'view_notification',    name='Can view notification',   content_type=content_type)
    
    # Obtiene los grupos
    group_admin         = Group.objects.get(name='Admin')
    group_staff         = Group.objects.get(name='Staff')
    group_client        = Group.objects.get(name='Default')
    
    # Agrega los permisos a los grupos Admin y Client
    group_admin.permissions.add(permission_add, permission_change, permission_delete, permission_view)
    group_staff.permissions.add(permission_view)
    group_client.permissions.add(permission_view)

    
class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        # Agrega aquí las operaciones de la migración.
        migrations.RunPython(create_initial_data),
    ]
