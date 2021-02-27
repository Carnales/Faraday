from django.contrib import admin
from .models import *

admin.site.register(Scientist)
admin.site.register(Employer)
admin.site.register(DataPool)
admin.site.register(DataEntry)