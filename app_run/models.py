from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    distance = models.FloatField(null=True)
    run_time_seconds = models.IntegerField(null=True)
    athlete = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='runs')


    class Status(models.TextChoices):
        INIT = 'init'
        IN_PROGRESS = 'in_progress'
        FINISHED = 'finished'

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.INIT)



class AthleteInfo(models.Model):
    goals = models.TextField(blank=True)
    weight = models.IntegerField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='athlete_info')



class Challenge(models.Model):
    full_name = models.CharField(max_length=50)
    athlete = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='challenge')



class Position(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    date_time = models.DateTimeField()
    run = models.ForeignKey(to=Run, on_delete=models.CASCADE, related_name='position')



class CollectibleItem(models.Model):
    name = models.CharField(max_length=50)
    uid = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    picture = models.URLField()
    value = models.IntegerField()
    athletes = models.ManyToManyField(to=User, related_name='collectibles')