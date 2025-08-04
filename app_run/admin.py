from django.contrib import admin
from .models import Run, Challenge, AthleteInfo
# Register your models here.

admin.site.register(Run)
admin.site.register(Challenge)
admin.site.register(AthleteInfo)