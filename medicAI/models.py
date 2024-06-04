from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):

    # Create constants to limit choices
    BLOOD_TYPE = [
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    dob = models.DateField()
    address = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    height = models.IntegerField(blank=True)
    weight = models.IntegerField(blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    ohip = models.CharField(max_length=12)
    blood_type = models.CharField(
        max_length=3, 
        choices=BLOOD_TYPE, 
        default="", 
        blank=True
    )

    def __str__(self):
        return f'ID: {self.id} | {self.first_name} {self.last_name}'


class Hospital_Visit(models.Model):

    ACUITY_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
        
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom_start_date = models.DateField(default=timezone.now, blank=True)
    acuity = models.CharField(max_length=1, choices=ACUITY_CHOICES, default='5')
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(45)]
    )
    heart_rate = models.IntegerField(null=True, blank=True)
    prescription = models.CharField(max_length=200, blank=True)
    diagnosis = models.CharField(max_length=200, blank=True)
    seen_nurse = models.BooleanField(default=False)
    er_doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    symptoms = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'Patient: {self.patient} | Date: {self.symptom_start_date}'


class Medical_Test(models.Model):
    hostpital_visit = models.ForeignKey(Hospital_Visit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=False)
    test_name = models.CharField(max_length=200, null=False, blank=False)
    test_notes = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'Test: {self.test_name}' 
    