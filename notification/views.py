from django.views.generic.list import ListView
from .models import Notification
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from django.shortcuts import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
    

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    # permission_required = 'notification.view_notification'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


@login_required
def Notification_ajax(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    data = []
    for notification in notifications:
        data.append({
            'title': notification.title,
            'description': notification.description,
            'created_at': timesince(notification.created_at),
            'url': notification.url
        })
    return JsonResponse(data, safe=False)

@login_required
def Notification_clear(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    notifications.update(seen=True)
    return HttpResponse(status=200)