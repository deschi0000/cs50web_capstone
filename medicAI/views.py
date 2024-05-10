from datetime import datetime
from django.http import HttpResponseRedirect
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

def edit_patient_info(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    current_visit = Hospital_Visit.objects.filter(id=patient_id).order_by('-symptom_start_date').first()

    if request.method == 'POST':
        print("trying to post form")

        #Retrieve the values of the input fields being Posted
        acuity = request.POST.get('acuity')
        temperature = request.POST.get('temperature')
        heart_rate = request.POST.get('heart_rate')
        symptom_start = request.POST.get('symptom_start')
        doctor_diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')

        seen_nurse = request.POST.get('seen_nurse') # Convert from str to bool
        if seen_nurse.lower() == 'true':
            seen_nurse = True
        else:
            seen_nurse = False
        
        print("===================================================")
        print(doctor_diagnosis)
        print(prescription)
        print("===================================================")

        current_visit.acuity = acuity
        current_visit.temperature = temperature
        current_visit.heart_rate = heart_rate
        current_visit.symptom_start_date = datetime.strptime(symptom_start,'%m/%d/%Y')
        current_visit.diagnosis = doctor_diagnosis
        current_visit.prescription = prescription
        current_visit.seen_nurse = seen_nurse
        current_visit.save()

        return HttpResponseRedirect(f"/patientinfo/{patient_id}")

    context = {
        'patient': patient,
        'current_visit': current_visit
    }
    return render(request, "medicAI/editpatientinfo.html", context) 
