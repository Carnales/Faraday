from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# datapool, user, employer

class Scientist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=0, null=True, blank=True)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class DataPool(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, blank=True, null=True)

class DataEntry(models.Model):
    scientist = models.OneToOneField(Scientist, on_delete=models.SET_NULL, null=True, blank=True)
    datapool = models.ForeignKey(DataPool, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    document = models.FileField(upload_to='documents/')

    accepted = models.BooleanField(default=False, null=True, blank=False)
    paid = models.BooleanField(default=False, null=True, blank=False)
