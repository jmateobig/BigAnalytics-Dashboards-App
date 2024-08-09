
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType


from dashboard.models import Dashboard

class DashboardListViewTest(TestCase):

    def setUp(self):
        # Crear un usuario con el permiso para ver el dashboard
        self.user = User.objects.create_user(username='testuser', password='12345')
        permission = Permission.objects.get(codename='view_dashboard')
        self.user.user_permissions.add(permission)
        self.user.save()

        # Crear algunos dashboards para la prueba
        Dashboard.objects.create(name='Dashboard_1', title='Title 1', description='Description 1', url='http://example.com/1')
        Dashboard.objects.create(name='Dashboard_2', title='Title 2', description='Description 2', url='http://example.com/2')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard:list'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/list')

    def test_logged_in_with_permission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard:list'))

        # Comprueba que el usuario está autorizado a ver la vista
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_list.html')

    def test_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard:list'))

        # Verifica que los dashboards están en el contexto
        self.assertTrue('dashboards' in response.context)
        self.assertEqual(len(response.context['dashboards']), 2)


class DashboardCreateViewTest(TestCase):

    def setUp(self):
        # Crear un usuario con el permiso para crear el dashboard
        self.user = User.objects.create_user(username='creator', password='12345')
        permission = Permission.objects.get(codename='add_dashboard')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='view_dashboard')
        self.user.user_permissions.add(permission)
        self.user.save()
        # Crear un grupo
        self.group = Group.objects.create(name='Test Group')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard:create'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/create')

    def test_logged_in_with_permission(self):
        self.client.login(username='creator', password='12345')
        response = self.client.get(reverse('dashboard:create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_create.html')

    def test_form_submission(self):
        self.client.login(username='creator', password='12345')
        data = {
            'name': 'New_Dashboard',
            'title': 'New Title',
            'description': 'New Description',
            'url': 'http://example.com'
        }
        response = self.client.post(reverse('dashboard:create'), data)
        self.assertRedirects(response, reverse('dashboard:list'))

        # Verifica que el dashboard fue creado
        dashboard = Dashboard.objects.get(name='New_Dashboard')
        self.assertIsNotNone(dashboard)


class DashboardRenderViewTest(TestCase):

    def setUp(self):
        # Crear un usuario y un dashboard con un permiso
        self.user = User.objects.create_user(username='user', password='12345')
        self.admin_group = Group.objects.create(name='admin')
        self.user.groups.add(self.admin_group)
        self.user.save()

        self.dashboard = Dashboard.objects.create(
            name='Dashboard_Test',
            title='Title Test',
            description='Description Test',
            url='http://example.com/test'
        )
        content_type = ContentType.objects.get_for_model(Dashboard)
        permission = Permission.objects.create(
            codename='can_read_dashboard_test',
            name='Can read Dashboard Test',
            content_type=content_type,
        )
        self.dashboard.permission = permission
        self.dashboard.save()

        self.admin_group.permissions.add(permission)

    def test_access_dashboard_with_permission(self):
        self.client.login(username='user', password='12345')
        url = reverse('dashboard:render', args=[self.dashboard.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_render.html')

    def test_access_dashboard_without_permission(self):
        self.client.logout()
        another_user = User.objects.create_user(username='another_user', password='12345')
        self.client.login(username='another_user', password='12345')
        url = reverse('dashboard:render', args=[self.dashboard.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Permission Denied