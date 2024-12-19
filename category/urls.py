from django.urls import path
from .views import  CategoryListView, CategoryListJsonView, CategoryDetailJsonView, CategoryEditView, CategoryDeleteView#, CategoryCreateView

app_name = 'category'

urlpatterns = [
    path('list',                       (CategoryListView.as_view()),           name='list'),
    path('api/categories',             (CategoryListJsonView.as_view()),       name='get_categories'),
    path('api/category/',              (CategoryDetailJsonView.as_view()),     name='get_category'),
    path('<int:pk>/edit/',             (CategoryEditView.as_view()),           name='edit'),
    path('api/category/delete/',       (CategoryDeleteView.as_view()),         name='delete'),
    # path('create',                     (CategoryCreateView.as_view()),         name='create'),
]



