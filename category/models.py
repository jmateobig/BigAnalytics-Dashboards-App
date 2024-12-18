from django.db import models
from django.contrib.auth.models import Group

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Agregar una relación de ForeignKey a Group
Group.add_to_class(
    'category',
    models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups', null=True, blank=True)
)