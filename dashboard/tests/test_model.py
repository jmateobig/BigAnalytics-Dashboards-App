from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from dashboard.models import Dashboard

class DashboardModelTest(TestCase):

    def setUp(self):
        self.permission = Permission.objects.create(
            codename='can_view_dashboard',
            name='Can View Dashboard',
            content_type_id=1
        )

    def test_create_dashboard(self):
        dashboard = Dashboard.objects.create(
            name='test_dashboard',
            title='Test Dashboard',
            description='This is a test dashboard.',
            url='https://example.com',
            permission=self.permission
        )
        self.assertEqual(dashboard.name, 'test_dashboard')
        self.assertEqual(dashboard.title, 'Test Dashboard')
        self.assertEqual(dashboard.description, 'This is a test dashboard.')
        self.assertEqual(dashboard.url, 'https://example.com')
        self.assertEqual(dashboard.permission, self.permission)

    def test_dashboard_name_no_spaces(self):
        with self.assertRaises(ValidationError):
            dashboard = Dashboard(
                name='test dashboard',  # El nombre contiene un espacio
                title='Test Dashboard',
                url='https://example.com'
            )
            dashboard.full_clean()  # Esto ejecuta la validación manualmente

    def test_dashboard_name_unique(self):
        dashboard1 = Dashboard.objects.create(
            name='unique_dashboard',
            title='Unique Dashboard',
            url='https://example.com',
            permission=self.permission
        )
        with self.assertRaises(ValidationError):
            dashboard2 = Dashboard(
                name='unique_dashboard',  # El nombre es el mismo que el del dashboard1
                title='Another Dashboard',
                url='https://example2.com'
            )
            dashboard2.full_clean()  # Ejecutar validación manual

    def test_dashboard_str_method(self):
        dashboard = Dashboard.objects.create(
            name='test_dashboard',
            title='Test Dashboard',
            url='https://example.com',
            permission=self.permission
        )
        self.assertEqual(str(dashboard), 'test_dashboard')