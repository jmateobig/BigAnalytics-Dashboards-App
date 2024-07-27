from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations


def create_initial_data(apps, schema_editor):
    # Crea un usuario en la tabla auth_user
    user = User.objects.create_superuser(username='jmateo', email='joubmaja.69@gmail.com', password='Cambiame123', first_name="Jonathan", last_name= "Mateo")
    user.save()
    
    staff = User.objects.create_user(username='jmateo_cys', email='jmateo.cys@gmail.com', password='Cambiame123', first_name="Ubaldo", last_name= "Jacinto")
    staff.save()
    
    client = User.objects.create_user(username='jmateo_big', email='jmateo@biganalytics.com.gt', password='Cambiame123', first_name="Vidal", last_name= "Hernandez")
    client.save()
    
    # Crea una dirección de correo electrónico verificada para el usuario
    email_address = EmailAddress(user=user, email='joubmaja.69@gmail.com', primary=True, verified=True)
    email_address.save()
    
    email_address_client = EmailAddress(user=staff, email='jmateo.cys@gmail.com', primary=True, verified=True)
    email_address_client.save()

    email_address_client = EmailAddress(user=client, email='jmateo@biganalytics.com.gt', primary=True, verified=True)
    email_address_client.save()
    
    # Crea los grupos en auth_group
    group_admin = Group(name='Admin')
    group_admin.save()

    group_staff = Group(name='Staff')
    group_staff.save()
    
    group_client= Group(name='Default')
    group_client.save()
    

    # Agrega el usuario al grupo
    user.groups.add(group_admin)
    staff.groups.add(group_staff)
    client.groups.add(group_client)
    
    # Crea el contenido para tu aplicación
    content_type = ContentType.objects.create(app_label='publicacion',model='user')
    
    # Crea los permisos para el modelo Users
    permission_add_user =       Permission.objects.create   (codename=  'add_user',         name='Can add user',        content_type=content_type)
    permission_change_user =    Permission.objects.create   (codename=  'change_user',      name='Can change user',     content_type=content_type)
    permission_delete_user =    Permission.objects.create   (codename=  'delete_user',      name='Can delete user',     content_type=content_type)
    permission_view_user =      Permission.objects.create   (codename=  'view_user',        name='Can view user',       content_type=content_type)
    permission_administration = Permission.objects.create   (codename=  'administration',   name='Can administration',  content_type=content_type)
    group_admin.permissions.add(permission_add_user,permission_change_user,permission_delete_user,permission_view_user, permission_administration)
    group_staff.permissions.add(permission_administration)
    
    
    content_type = ContentType.objects.create(app_label='publicacion',model='group')
    # Crea los permisos para el modelo Users
    permission_add_group =      Permission.objects.create   (codename=  'add_group',     name='Can add user',    content_type=content_type)
    permission_change_group =   Permission.objects.create   (codename=  'change_group',  name='Can change user', content_type=content_type)
    permission_delete_group =   Permission.objects.create   (codename=  'delete_group',  name='Can delete user', content_type=content_type)
    permission_view_group =     Permission.objects.create   (codename=  'view_group',    name='Can view user',   content_type=content_type)
    group_admin.permissions.add(permission_add_group,permission_change_group,permission_delete_group,permission_view_group)
    
    
    
    
class Migration(migrations.Migration):
    dependencies = [
        # Agrega aquí las dependencias de la migración.
    ]

    operations = [
        # Agrega aquí las operaciones de la migración.
        migrations.RunPython(create_initial_data),
    ]
