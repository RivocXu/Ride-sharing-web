from django.db import models
from django.urls import reverse


# Create your models here.
class RideUser(models.Model):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )

    name = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=68, choices=gender, default='male')
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'User'
        verbose_name_plural = 'User'


class Vehicle(models.Model):
    owner = models.OneToOneField(RideUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=False, default='xxx')
    license_num = models.CharField(max_length=100, null=False, default='xxx')
    capacity = models.IntegerField(default=4, null=False)
    otherInfo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f' {self.owner.name} {self.license_num} '


class Ride(models.Model):
    owner = models.ForeignKey(RideUser, on_delete=models.CASCADE,related_name='owner')
    sharer = models.ManyToManyField(RideUser,related_name='sharer',blank=True)
    driver = models.ForeignKey(RideUser,on_delete=models.CASCADE,related_name='driver',blank=True,null=True)

    STATUS = (
        ('open', 'open'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )
    status = models.CharField(default='open', max_length=20, choices=STATUS)
    is_Share = models.BooleanField(default=False,blank=True)
    destination = models.CharField(max_length=100,blank=False)
    arrival_time = models.DateTimeField(null=True,blank=False)
    capacity = models.IntegerField(default=0,blank=False)
    vehicle_type = models.CharField(max_length=50, blank=True)
    special_request = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.owner.name} {self.destination}'





