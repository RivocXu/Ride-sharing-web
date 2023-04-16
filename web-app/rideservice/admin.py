from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.RideUser)
admin.site.register(models.Vehicle)
admin.site.register(models.Ride)