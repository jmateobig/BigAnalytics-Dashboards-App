from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import (
    DashboardListView,
    DashboardCreateView,
    DashboardListJsonView,
    DashboardDetailJsonView,
    DashboardEditView,
    DashboardDeleteView,
    DashboardRenderView
)

class TestDashboardUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('dashboard:list')
        self.assertEqual(resolve(url).func.view_class, DashboardListView)

    def test_get_dashboards_url_resolves(self):
        url = reverse('dashboard:get_dashboards')
        self.assertEqual(resolve(url).func.view_class, DashboardListJsonView)

    def test_create_url_resolves(self):
        url = reverse('dashboard:create')
        self.assertEqual(resolve(url).func.view_class, DashboardCreateView)

    def test_get_dashboard_url_resolves(self):
        url = reverse('dashboard:get_dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardDetailJsonView)

    def test_edit_url_resolves(self):
        url = reverse('dashboard:edit', args=[1])
        self.assertEqual(resolve(url).func.view_class, DashboardEditView)

    def test_delete_url_resolves(self):
        url = reverse('dashboard:delete')
        self.assertEqual(resolve(url).func.view_class, DashboardDeleteView)

    def test_render_url_resolves(self):
        url = reverse('dashboard:render', args=[1])
        self.assertEqual(resolve(url).func.view_class, DashboardRenderView)