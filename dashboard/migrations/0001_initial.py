from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations


def create_initial_data(apps, schema_editor):
    
    # Crea el contenido para tu aplicación
    content_type = ContentType.objects.create(app_label='dashboard',model='dashboard')

    # Obtiene los grupos
    group_admin         = Group.objects.get(name='Admin')
    group_client        = Group.objects.get(name='Default')
    
    # Crea los permisos para el modelo dashboard
    permission_add =    Permission.objects.create       (codename=  'add_dashboard',     name='Can add dashboard',    content_type=content_type)
    permission_change = Permission.objects.create       (codename=  'change_dashboard',  name='Can change dashboard', content_type=content_type)
    permission_delete = Permission.objects.create       (codename=  'delete_dashboard',  name='Can delete dashboard', content_type=content_type)
    permission_view =   Permission.objects.create       (codename=  'view_dashboard',    name='Can view dashboard',   content_type=content_type)
    
    # Agrega los permisos a los grupos Admin y Client
    group_admin.permissions.add(permission_add,permission_change,permission_delete,permission_view)
    group_client.permissions.add(permission_view)
    
    
    
    
class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        # Agrega aquí las operaciones de la migración.
        migrations.RunPython(create_initial_data),
    ]
