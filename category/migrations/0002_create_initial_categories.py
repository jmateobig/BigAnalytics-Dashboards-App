from django.db import migrations, models

def create_categories_and_assign_groups(apps, schema_editor):
    # Obtener los modelos dinámicamente para evitar problemas de importación directa
    Category = apps.get_model('category', 'Category')
    Group = apps.get_model('auth', 'Group')

    # Crear las categorías
    category1 = Category.objects.create(name="Categoria 1", description="Descripción para Categoria 1")
    Category.objects.create(name="Categoria 2", description="Descripción para Categoria 2")
    Category.objects.create(name="Categoria 3", description="Descripción para Categoria 3")

    # Asignar todos los grupos existentes a "Categoria 1"
    groups = Group.objects.all()
    for group in groups:
        group.category = category1
        group.save()

class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),  # Asegúrate de que apunte a la migración inicial de tu app
        ('auth', '0012_alter_user_first_name_max_length'),  # Dependencia de las migraciones de auth
    ]

    operations = [
        migrations.RunPython(create_categories_and_assign_groups),
    ]
