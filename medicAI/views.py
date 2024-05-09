from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

from medicAI.models import Hospital_Visit, Patient

# Create your views here.


def index(request):

    return render(request, "medicAI/index.html")

def patientlist(request):

    # Use try/except to find patients in the db
    # all_patients = Patient.objects.all()
    # context = {
    #     "patients": all_patients,
    # }
    # return render(request, "medicAI/index.html", context)

    # Get all of the hospital visits and also the information
    # of each of the patients as well
    # all_hospital_visits = Hospital_Visit.objects.all()
    all_hospital_visits = Hospital_Visit.objects.all().order_by('acuity')
    print(all_hospital_visits)
    context = {
        "hospital_visits": all_hospital_visits
    }
    return render(request, "medicAI/patientlist.html", context)

def patient_info(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    # print(patient.first_name)

    # Get the most recent visit
    visit_list = Hospital_Visit.objects.filter(id=patient_id).order_by('-symptom_start_date')
    most_recent_visit = visit_list.first()
    # for i in visit_list:       # for debugging if checking for multiple visits.
    #     print(i)

    context= {
        'patient': patient,
        'visit_list' : visit_list,
        'current_visit': most_recent_visit
    }

    return render(request, "medicAI/patientinfo.html", context)
