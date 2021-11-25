from django.db import models
from django.db.models.fields import TextField

# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')