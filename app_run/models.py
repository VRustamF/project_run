from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.TextField()

    class Status(models.TextChoices):
        INIT = 'init'
        IN_PROGRESS = 'in_progress'
        FINISHED = 'finished'

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.INIT)

