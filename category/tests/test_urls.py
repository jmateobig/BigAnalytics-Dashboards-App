from django.test import SimpleTestCase
from django.urls import reverse, resolve
from category.views import (
    CategoryListView,
    CategoryListJsonView,
    CategoryDetailJsonView,
    CategoryEditView,
    CategoryDeleteView,
    CategoryCreateView
)

class TestCategoryUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('category:list')
        self.assertEqual(resolve(url).func.view_class, CategoryListView)

    def test_get_categories_url_resolves(self):
        url = reverse('category:get_categories')
        self.assertEqual(resolve(url).func.view_class, CategoryListJsonView)

    def test_get_category_url_resolves(self):
        url = reverse('category:get_category')
        self.assertEqual(resolve(url).func.view_class, CategoryDetailJsonView)

    def test_edit_url_resolves(self):
        url = reverse('category:edit', args=[1])  # `args` pasa un `pk` ficticio
        self.assertEqual(resolve(url).func.view_class, CategoryEditView)

    def test_delete_url_resolves(self):
        url = reverse('category:delete')
        self.assertEqual(resolve(url).func.view_class, CategoryDeleteView)

    def test_create_url_resolves(self):
        url = reverse('category:create')
        self.assertEqual(resolve(url).func.view_class, CategoryCreateView)
