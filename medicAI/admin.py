from django.contrib import admin
from .models import Patient, Hospital_Visit

# Register your models here.

admin.site.register(Patient)
admin.site.register(Hospital_Visit)
