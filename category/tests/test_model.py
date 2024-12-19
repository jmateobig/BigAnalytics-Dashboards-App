from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from category.models import Category

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category.'
        )
        self.group1 = Group.objects.create(name='Group One')
        self.group2 = Group.objects.create(name='Group Two')

    def test_create_category(self):
        category = Category.objects.create(
            name='Another Category',
            description='Another test description.'
        )
        self.assertEqual(category.name, 'Another Category')
        self.assertEqual(category.description, 'Another test description.')

    def test_category_name_unique(self):
        with self.assertRaises(ValidationError):
            duplicate_category = Category(
                name='Test Category',  # Nombre ya existente
                description='Duplicate description.'
            )
            duplicate_category.full_clean()  # Ejecutar validación manual

    def test_category_name_max_length(self):
        long_name = 'A' * 256  # Supera el límite de 255 caracteres
        with self.assertRaises(ValidationError):
            category = Category(
                name=long_name,
                description='This is a test with a very long name.'
            )
            category.full_clean()  # Ejecutar validación manual

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_assign_groups_to_category(self):
        self.group1.category = self.category
        self.group1.save()

        self.group2.category = self.category
        self.group2.save()

        self.assertIn(self.group1, self.category.groups.all())
        self.assertIn(self.group2, self.category.groups.all())

    def test_remove_group_from_category(self):
        # Asignar un grupo a la categoría
        self.group1.category = self.category
        self.group1.save()

        # Eliminar la relación con la categoría
        self.group1.category = None
        self.group1.save()

        self.assertNotIn(self.group1, self.category.groups.all())
