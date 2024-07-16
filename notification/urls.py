from django.urls import path
from .views import NotificationListView, Notification_ajax, Notification_clear

app_name = 'notification'

urlpatterns = [
    path('',                NotificationListView.as_view(), name='list'),
    path('notification',    Notification_ajax,              name='ajax'),
    path('clear',           Notification_clear,             name='clear'),
]