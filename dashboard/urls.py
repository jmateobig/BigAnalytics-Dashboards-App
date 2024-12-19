from django.urls import path
from .views import  DashboardListView, DashboardCreateView, DashboardListJsonView, DashboardDetailJsonView, DashboardEditView, DashboardDeleteView, DashboardRenderView

app_name = 'dashboard'

urlpatterns = [
    path('list',                       (DashboardListView.as_view()),           name='list'),
    path('api/dashboards',             (DashboardListJsonView.as_view()),       name='get_dashboards'),
    path('create',                     (DashboardCreateView.as_view()),         name='create'),
    path('api/dashboard/',             (DashboardDetailJsonView.as_view()),     name='get_dashboard'),
    path('<int:dashboard_id>/edit/',   (DashboardEditView.as_view()),           name='edit'),
    path('api/dashboard/delete/',      (DashboardDeleteView.as_view()),         name='delete'),
    path('render/<int:dashboard_id>/', (DashboardRenderView.as_view()),         name='render'),
]



