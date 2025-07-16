from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.TextField()

