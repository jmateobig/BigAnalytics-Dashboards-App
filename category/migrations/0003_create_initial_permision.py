from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations


def create_initial_data(apps, schema_editor):
    
    # Crea el contenido para tu aplicación
    content_type     = ContentType.objects.create(app_label='category',model='category')

    # Obtiene los grupos
    group_admin         = Group.objects.get(name='Admin')
    group_staff         = Group.objects.get(name='Staff')
    
    # Crea los permisos para el modelo category
    # permission_add =    Permission.objects.create       (codename=  'add_category',     name='Can add category',    content_type=content_type)
    permission_change = Permission.objects.create       (codename=  'change_category',  name='Can change category', content_type=content_type)
    permission_delete = Permission.objects.create       (codename=  'delete_category',  name='Can delete category', content_type=content_type)
    permission_view =   Permission.objects.create       (codename=  'view_category',    name='Can view category',   content_type=content_type)
    
    # Agrega los permisos a los grupos Admin y Client
    # group_admin.permissions.add(permission_add,permission_change,permission_delete,permission_view)
    # group_staff.permissions.add(permission_add,permission_change,permission_delete,permission_view)
    group_admin.permissions.add(permission_change,permission_delete,permission_view)
    group_staff.permissions.add(permission_change,permission_delete,permission_view)

class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_create_initial_categories'),
    ]

    operations = [
        # Agrega aquí las operaciones de la migración.
        migrations.RunPython(create_initial_data),
    ]