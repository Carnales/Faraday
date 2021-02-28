from django.db import models
from django.contrib.auth.models import User
import csv, itertools

# Create your models here.

# datapool, user, employer

class Scientist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=25, null=True)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class DataPool(models.Model):
    name = models.CharField(max_length=25, null=True)
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, blank=True, null=True)

    questions = models.TextField(default="Ask your questions here!", max_length=300, blank=True, null=True)

    description = models.CharField(max_length=50, null=True)

    COLOR_CHOICES = (
        ('Ecology','ECOLOGY'),
        ('Sociology', 'SOCIOLOGY'),
        ('Astronomy','ASTRONOMY'),
        ('Geology','GEOLOGY')
        )

    category = models.CharField(max_length=25, choices=COLOR_CHOICES, default='Ecology')

    entry_cap = models.IntegerField(default=100, null=True, blank=True)

    @property
    def prize(self):
        # print(self.document.url)
        # print("================================================================")
        # with open('static/images/references' + self.document.url) as csvfile:
        #         content = csv.reader(csvfile, delimiter=' ', quotechar='|')
        #         content = list(content)
        #         return len(content)
        return len(self.questions.split(','))*0.25-0.01

class DataEntry(models.Model):
    scientist = models.ForeignKey(Scientist, on_delete=models.SET_NULL, null=True, blank=True)
    datapool = models.ForeignKey(DataPool, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=2, default='US')

    answers = models.TextField(default="Answer the questions here!", max_length=300, blank=True, null=True)

    accepted = models.BooleanField(default=False, null=True, blank=False)
    paid = models.BooleanField(default=False, null=True, blank=False)