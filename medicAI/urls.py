from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patientinfo/<str:patient_id>", views.patient_info, name="patientinfo")
]