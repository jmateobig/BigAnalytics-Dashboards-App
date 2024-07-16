from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    seen = models.BooleanField(default=False)
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_notification'