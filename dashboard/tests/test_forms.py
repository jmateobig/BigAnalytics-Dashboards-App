from django.test import TestCase
from django.contrib.auth.models import User, Group
from dashboard.forms import DashboardCreateForm, DashboardEditForm

class DashboardCreateFormTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='User One', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', first_name='User Two', email='user2@example.com')
        self.group1 = Group.objects.create(name='Group One')
        self.group2 = Group.objects.create(name='Group Two')

    def test_dashboard_create_form_valid(self):
        form_data = {
            'name': 'Test_Dashboard',
            'title': 'Test Title',
            'description': 'Test Description',
            'url': 'https://example.com',
            'groups': [self.group1.id, self.group2.id],
            'users': [self.user1.id, self.user2.id],
        }
        form = DashboardCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dashboard_create_form_invalid_without_name(self):
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'url': 'https://example.com',
            'groups': [self.group1.id, self.group2.id],
            'users': [self.user1.id, self.user2.id],
        }
        form = DashboardCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_user_label_from_instance(self):
        form = DashboardCreateForm()
        label = form.user_label_from_instance(self.user1)
        self.assertEqual(label, 'User One (user1@example.com)')


class DashboardEditFormTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='User', last_name='One', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', first_name='User', last_name='Two', email='user2@example.com')
        self.group1 = Group.objects.create(name='Group One')
        self.group2 = Group.objects.create(name='Group Two')

    def test_dashboard_edit_form_valid(self):
        form_data = {
            'name': 'Test_Dashboard',
            'title': 'Test Title',
            'description': 'Test Description',
            'url': 'https://example.com',
            'groups': [self.group1.id, self.group2.id],
            'users': [self.user1.id, self.user2.id],
        }
        form = DashboardEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dashboard_edit_form_invalid_without_title(self):
        form_data = {
            'name': 'Test Dashboard',
            'description': 'Test Description',
            'url': 'https://example.com',
            'groups': [self.group1.id, self.group2.id],
            'users': [self.user1.id, self.user2.id],
        }
        form = DashboardEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_user_label_from_instance(self):
        form = DashboardEditForm()
        label = form.user_label_from_instance(self.user1)
        self.assertEqual(label, 'User One (user1@example.com)')
