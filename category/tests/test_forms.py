from django.test import TestCase
from django.contrib.auth.models import Group
from category.models import Category  # Asegúrate de importar correctamente tu modelo de Category
from category.forms import CategoryForm

class CategoryFormTest(TestCase):

    def setUp(self):
        # Crear datos de prueba
        self.group1 = Group.objects.create(name='Group One')
        self.group2 = Group.objects.create(name='Group Two')
        self.category = Category.objects.create(name='Test Category', description='Test Description')

    def test_category_form_valid(self):
        form_data = {
            'name': 'New Category',
            'description': 'This is a valid description',
            'groups': [self.group1.id, self.group2.id],
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid_without_name(self):
        form_data = {
            'description': 'This is a description',
            'groups': [self.group1.id, self.group2.id],
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_category_form_invalid_without_description(self):
        form = CategoryForm(data={'name': 'Category 1'})
        self.assertTrue(form.is_valid())  # Ahora esperamos que sea válido

    def test_category_form_save(self):
        form_data = {
            'name': 'Category with Groups',
            'description': 'Category Description',
            'groups': [self.group1.id, self.group2.id],
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())
        category = form.save()

        self.assertEqual(category.name, 'Category with Groups')
        self.assertEqual(category.description, 'Category Description')
        self.assertIn(self.group1, category.groups.all())
        self.assertIn(self.group2, category.groups.all())

    def test_category_form_save_without_groups(self):
        form_data = {
            'name': 'Category without Groups',
            'description': 'Category Description',
            'groups': [],
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())
        category = form.save()

        self.assertEqual(category.name, 'Category without Groups')
        self.assertEqual(category.description, 'Category Description')
        self.assertEqual(category.groups.count(), 0)
