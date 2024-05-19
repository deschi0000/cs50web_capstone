from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patientlist", views.patientlist, name="patientlist"),
    path("patientinfo/<str:patient_id>", views.patient_info, name="patientinfo"),
    path("patientinfo/<str:patient_id>/edit", views.edit_patient_info, name="editpatientinfo"),
    path("d", views.diagnosis, name="diagnosis")
]