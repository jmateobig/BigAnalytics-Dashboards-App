from django.urls import path
from .views import  DashboardListView, DashboardListJsonView, DashboardCreateView#, GroupCreateView, GroupEditView, GroupDeleteView

app_name = 'dashboard'

urlpatterns = [
    path('list',                     (DashboardListView.as_view()),           name='list'),
    path('api/dashboards',           (DashboardListJsonView.as_view()),       name='get_dashboards'),
    path('create',                   (DashboardCreateView.as_view()),         name='create'),
    # path('api/group/',               (GroupDetailJsonView.as_view()),       name='get_group'),
    # path('group/create/',            (GroupCreateView.as_view()),           name='create'),
    # path('edit/<int:group_id>/',     (GroupEditView.as_view()),             name='edit'),
    # path('api/group/delete/',        (GroupDeleteView.as_view()),           name='delete_group'),
]



