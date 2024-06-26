
# CS50Web Capstone Project

Dave von Deschwanden

### Summary

I wanted to create something that could both demonstrate the skills I've learned throughout this course and have potential real-world benefits. Since there is a strain on the Canadian health care system, resulting in overworked medical workers, the idea to make an AI-aid for diagnosing patients, would help streamline the work for doctors and nurses, and also reduce the potential of misdiagnoses.

This system focuses more on the user as a medical professional; the patients already registered in the system are done so using a stub which at this point in development represents the user already being registered and having described their symptoms (a self-check in system would be really cool, although this could also just have been done manually), as such the patients are already registered with symptoms. 

The next step was finding the right API that would be able to take these symptoms and convert them into a meaningful diagnosis. This was found in the apiMedic. Our application will continually update itself depending on the symptoms listed for each individual patient. The diagnoses hold medical information, as well as the likelihood as a percentage of it being the correct one for the patient.

OpenAI capability was used to elaborate on any suggested diagnoses, providing another quickly accessible second opinion that may be useful in the treatement of a patient.

The rest of the application utilized the user model (medical professional), making sure to hide sensitive patient data from anyone not authorized to use the system. In lew of registering, the assumption for this application is that the system administrator of the hospital has added authorized personal into the system.



### Distinctiveness

This project is distintive in that it serves as a tool to aid ER medical staff in making decisions based on their patients. Aside from mostly pure CSS in the previous projects, this applicaiton makes bootstrap and the fontawesome libraries to help make the site more user-friendly and mobile responsive. 


### Complexity

The medical API used in this project is different from others I've used in the past in that it requires to load a time-sensitive token when making calls. Finding out the correct implementation and understanding how to properly utlize it in this project was a challenge. Also making use of the OpenAI developer tools, finding a way to prompt an explanation for certain daignoses being registered was interesting.

### Tech Stack

Django, Javascript, HTML, CSS, 

