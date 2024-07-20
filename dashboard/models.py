from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission

def validate_no_spaces(value):
    if ' ' in value:
        raise ValidationError('El nombre no puede contener espacios.')

class Dashboard(models.Model):
    name = models.CharField(max_length=150, unique=True, validators=[validate_no_spaces])
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name