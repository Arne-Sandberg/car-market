from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    owner = models.CharField(max_length=70)
