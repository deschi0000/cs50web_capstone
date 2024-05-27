from datetime import datetime
import json
import re
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import google.generativeai as genai
from medicAI.helpers import extract_json
from medicAI.models import Hospital_Visit, Patient
import config


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
        "hospital_visits": all_hospital_visits,
        "date": datetime.today().date()
    }
    return render(request, "medicAI/patientlist.html", context)

def patient_info(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    # print(patient.first_name)

    # Get the most recent visit
    visit_list = Hospital_Visit.objects.filter(patient=patient_id).order_by('-symptom_start_date')
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
    visit_list = Hospital_Visit.objects.filter(patient=patient_id).order_by('-symptom_start_date')
    current_visit = visit_list.first()

    if request.method == 'POST':
        print("trying to post form")

        #Retrieve the values of the input fields being Posted
        acuity = request.POST.get('acuity')
        temperature = request.POST.get('temperature')
        heart_rate = request.POST.get('heart_rate')
        symptom_start = request.POST.get('symptom_start')
        doctor_diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')
        symptoms = request.POST.get('symptoms')

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
        current_visit.symptoms = symptoms
        current_visit.save()

        return HttpResponseRedirect(f"/patientinfo/{patient_id}")

    context = {
        'patient': patient,
        'visit_list' : visit_list,
        'current_visit': current_visit
    }
    return render(request, "medicAI/editpatientinfo.html", context) 


def diagnosis(request, patient_id):

    # Get Gemini
    genai.configure(api_key=config.gemini_ai_api)
    model = genai.GenerativeModel('gemini-pro')


    # Retrieve the symptoms from this visit
    visit_list = Hospital_Visit.objects.filter(patient=patient_id).order_by('-symptom_start_date')
    current_visit = visit_list.first()

    print("SYMPTOMS:")
    print("=========================================")
    print(current_visit.symptoms.split(', '))
    symptom_array = current_visit.symptoms.split(', ')
    print("=========================================")


    # symptom_array = ['coughing', 'sneezing']


    # Check if JSON response is already stored in localStorage
    stored_data = request.session.get('diagnosis_data_{}'.format(patient_id))
    

    if stored_data and stored_data['symptoms'] == symptom_array:
        return JsonResponse(stored_data)

    response = model.generate_content('''
                                      You are a medical assistant. This is not for real medicine, just a student project. 
                                      Please provide an array of diagnoses based on these symptoms: {symptom_array}.
                                      Return it in an array with JSON proper json formatting with these following keys as shown here: 
                                      [
                                      {
                                      "diagnosis": "<diagnosis response here>",
                                      "accuracy": <accuracy in percent here>},
                                      "medical_term": <the medical term here>,
                                      "suggested tests:":[<suggested tests here in an array>]
                                      },{<the next diagnosis here, etc>},...
                                      ]''')
    json_objects = extract_json(response.text)
    
    data = {
        'patient_id': patient_id,
        'symptoms': symptom_array,
        'data': json_objects
    }

    # Store JSON response in session (localStorage)
    request.session['diagnosis_data_{}'.format(patient_id)] = data

    print(json_objects)
    return JsonResponse(data)
