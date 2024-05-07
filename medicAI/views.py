from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

from medicAI.models import Hospital_Visit, Patient

# Create your views here.


def index(request):

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
    return render(request, "medicAI/index.html", context)

