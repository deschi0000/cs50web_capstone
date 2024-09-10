from datetime import datetime
import json
import re
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import google.generativeai as genai
from medicAI.helpers import extract_json
from medicAI.models import Hospital_Visit, Patient, Medical_Test
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

    # Recieve the appropriate tests for the hostipal visit / patient
    tests = Medical_Test.objects.filter(hospital_visit=most_recent_visit)
    # print(tests)

    # Set a current patient so that the ID can be pulled when adding tests
    # (this will get reset by navigating throught the corres. urls...)
    current_patient = request.session['current_patient'] = patient_id

    context= {
        'patient': patient,
        'visit_list' : visit_list,
        'current_visit': most_recent_visit,
        'tests': tests
    }

    return render(request, "medicAI/patientinfo.html", context)

def edit_patient_info(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    visit_list = Hospital_Visit.objects.filter(patient=patient_id).order_by('-symptom_start_date')
    current_visit = visit_list.first()
    tests = Medical_Test.objects.filter(hospital_visit=current_visit)


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
        'current_visit': current_visit,
        'tests': tests
    }
    return render(request, "medicAI/editpatientinfo.html", context) 


def diagnosis(request, patient_id):

    # Get Gemini
    genai.configure(api_key=config.gemini_ai_api)
    model = genai.GenerativeModel('gemini-pro')


    # Retrieve the symptoms from this visit
    visit_list = Hospital_Visit.objects.filter(patient=patient_id).order_by('-symptom_start_date')
    current_visit = visit_list.first()
    tests_in_db = Medical_Test.objects.filter(hospital_visit=current_visit)
    tests_in_db = [i.test_name.strip() for i in tests_in_db]
    # print("THESE TESTS FOR PATIENT:")
    # print(tests_in_db)

    # print("SYMPTOMS:")
    # print("=========================================")
    # print(current_visit.symptoms.split(', '))
    symptom_array = current_visit.symptoms.split(', ')
    # print("=========================================")



    # Check if JSON response is already stored in localStorage
    data = request.session.get('diagnosis_data_{}'.format(patient_id))
    
    # # Get the suggested test list
    # suggested_test_list = [i['suggested_tests'] for i in data['data']]
    # # flatten out the array of arrays
    # flat_list = [item for sublist in suggested_test_list for item in sublist]
    # data['flat_list'] = flat_list


    if data and data['symptoms'] == symptom_array:
        # return JsonResponse(data)
        # Add the tests already in the system
        # Compare this set to the list and list any minuses for the tests that can be removed
        data['tests_in_db'] = tests_in_db
        # stored_data['tests_in_system'] = list(tests_in_db.values_list('test_name', flat=True))
        
        # Get the suggested tests out of the data list into an array


        # print("THESE TESTS FOR PATIENT:")
        # print(stored_data['tests_in_system'])
        print("=============================================")

        print(tests_in_db)
        print("=============================================")


        return render(request, "medicAI/diagnosislist.html", data) 
    
    response = model.generate_content('''
                                      You are a medical assistant. This is not for real medicine, just a student project. 
                                      Please provide an array of diagnoses based on these symptoms: {symptom_array}.
                                      Return it in an array with JSON proper json formatting with these following keys as shown here: 
                                      [
                                      {
                                      "diagnosis": "<diagnosis response here>",
                                      "accuracy": <accuracy in percent here>},
                                      "medical_term": <the medical term here>,
                                      "suggested_tests:":[<suggested tests here in an array>]
                                      },{<the next diagnosis here, etc>},...
                                      ]''')
    json_objects = extract_json(response.text)
    
    data = {
        'patient_id': patient_id,
        'symptoms': symptom_array,
        'data': json_objects,
        'tests_in_db': tests_in_db,
        # 'flat_list': flat_list
    }

    # Store JSON response in session (localStorage)
    request.session['diagnosis_data_{}'.format(patient_id)] = data

    print(json_objects)
    # return JsonResponse(data)

    return render(request, "medicAI/diagnosislist.html", data) 

def delete_test_edit_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("getting it here on the backend!!===================")
        
        test_name = data.get('test')
        test_name = test_name.strip()
        test_name = " " + test_name
        print("the test:")
        print(test_name)
        current_patient_id = request.session.get('current_patient')
        current_hospital_visit = Hospital_Visit.objects.filter(patient=current_patient_id).first()
        print(current_hospital_visit)
        
        test_in_db = Medical_Test.objects.filter(hospital_visit=current_hospital_visit)
        print("WHAT IS TEST_IN_DB??0")
        print(test_in_db)
        test_in_db = test_in_db.filter(test_name = test_name).first()
        

        print("WHAT IS TEST_IN_DB??1")
        print(test_in_db)
        if test_in_db:
            # TODO - Right now it will delete it with the fetch, 
            # but the data will not persist in the database~~~
            test_in_db.delete()
            return JsonResponse({'message': 'Test removed successfully'})
        else:
             return JsonResponse({'message': 'test not in the databse'})
    else:
        return JsonResponse({'message': 'test not removed successfully'})


def add_test(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        test_name = data.get('test')
        current_patient_id = request.session.get('current_patient')
        print(f"current patient id: {id}")

        # get the hospital visit queryset
        current_hospital_visit = Hospital_Visit.objects.filter(patient=current_patient_id).first()
        print("current visit:")
        print(current_hospital_visit)

        # check to see if the medical test is in the db
        test_in_db = Medical_Test.objects.filter(hospital_visit=current_hospital_visit)
        test_in_db = test_in_db.filter(test_name = test_name).first()
        print("---IN THE DB")
        print(test_in_db)

        if test_in_db:
            print("Yes it is, removing it")
            test_in_db.delete()

        else:
            print("test not yet in DB, putting it in")
            test_to_add = Medical_Test(
            hospital_visit=current_hospital_visit,
            test_name=test_name
            )
            test_to_add.save()

        return JsonResponse({'message': 'Test modified successfully'})
    else:
        return JsonResponse({'message': 'no test added successfully'})