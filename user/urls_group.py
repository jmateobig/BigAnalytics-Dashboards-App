from django.urls import path
from .views_group import  GroupListView, GroupListJsonView, GroupDetailJsonView, GroupCreateView, GroupEditView, GroupDeleteView

app_name = 'group'

urlpatterns = [
    path('list',                     (GroupListView.as_view()),             name='list'),
    path('api/groups',               (GroupListJsonView.as_view()),         name='get_groups'),
    path('api/group/',               (GroupDetailJsonView.as_view()),       name='get_group'),
    path('group/create/',            (GroupCreateView.as_view()),           name='create'),
    path('edit/<int:group_id>/',     (GroupEditView.as_view()),             name='edit'),
    path('api/group/delete/',        (GroupDeleteView.as_view()),           name='delete_group'),
]



