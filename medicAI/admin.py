from django.contrib import admin
from .models import Patient, Hospital_Visit, Medical_Test

# Register your models here.

admin.site.register(Patient)
admin.site.register(Hospital_Visit)
admin.site.register(Medical_Test)
