from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from category.models import Category

class CategoryListViewTest(TestCase):

    def setUp(self):
        # Crear un usuario con el permiso para ver categorías
        self.user = User.objects.create_user(username='testuser', password='12345')
        permission = Permission.objects.get(codename='view_category')
        self.user.user_permissions.add(permission)
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('category:list'))
        self.assertRedirects(response, '/accounts/login/?next=/category/list')

    def test_logged_in_with_permission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('category:list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')

    def test_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('category:list'))

        self.assertTrue('category' in response.context)
        self.assertEqual(len(response.context['category']), 3)


class CategoryCreateViewTest(TestCase):

    def setUp(self):
        # Crear un usuario con el permiso para agregar categorías
        self.user = User.objects.create_user(username='creator', password='12345')
        permission = Permission.objects.get(codename='add_category')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='view_category')
        self.user.user_permissions.add(permission)
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('category:create'))
        self.assertRedirects(response, '/accounts/login/?next=/category/create')

    def test_logged_in_with_permission(self):
        self.client.login(username='creator', password='12345')
        response = self.client.get(reverse('category:create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_create.html')

    def test_form_submission(self):
        self.client.login(username='creator', password='12345')
        data = {
            'name': 'New_Category',
            'description': 'New Description',
        }
        response = self.client.post(reverse('category:create'), data)
        self.assertRedirects(response, reverse('category:list'))

        # Verifica que la categoría fue creada
        category = Category.objects.get(name='New_Category')
        self.assertIsNotNone(category)


class CategoryDeleteViewTest(TestCase):

    def setUp(self):
        # Crear un usuario con el permiso para eliminar categorías
        self.user = User.objects.create_user(username='deleter', password='12345')
        self.category = Category.objects.create(name='Category_1', description='Description 1')
        self.group = Group.objects.create(name='Test Group', category=self.category)

    def test_delete_category(self):
        self.client.login(username='deleter', password='12345')

        response = self.client.post(
            reverse('category:delete'), 
            {'category_id': self.category.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode(),
            {'status': 'success', 'message': 'Categoría eliminada con éxito'}
        )
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class CategoryDetailJsonViewTest(TestCase):

    def setUp(self):
        # Crear una categoría y algunos grupos asociados
        self.category = Category.objects.create(name='Category_1', description='Description 1')
        self.group1 = Group.objects.create(name='Group_1', category=self.category)
        self.group2 = Group.objects.create(name='Group_2', category=self.category)

    def test_get_category_details(self):
        response = self.client.post(
            reverse('category:get_category'),
            {'category_id': self.category.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode(),
            {
                'status': 'success',
                'data': {
                    'id': self.category.id,
                    'name': 'Category_1',
                    'description': 'Description 1',
                    'groups': ['Group_1', 'Group_2'],
                }
            }
        )
