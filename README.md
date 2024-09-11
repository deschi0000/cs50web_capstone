
# CS50Web Capstone Project

Dave von Deschwanden

### Summary

I wanted to create something that could both demonstrate the skills I've learned throughout this course and have potential real-world benefits. Since there is a strain on the Canadian health care system, resulting in overworked medical workers, the idea to make an AI-aid for diagnosing patients, would help streamline the work for doctors and nurses, and also reduce the potential of misdiagnoses.

This system focuses more on the user as a medical professional; the patients already registered in the system are done so using a stub which at this point in development represents the user already being registered and having described their symptoms (a self-check in system would be really cool, although this could also just have been done manually), as such the patients are already registered with symptoms. 

The next step is was using the Gemini API that would take these symptoms and convert them into a meaningful possible diagnoses. The application will continually update itself depending on the symptoms listed for each individual patient. It will also output the diagnoses in descending percentages of possibility, along with the associated tests that can be added or removed for the patient. 

This capability would be helpful to be used to help elaborate on any suggested diagnoses, providing another quickly accessible second opinion that may be useful in the treatement of a patient.

The rest of the application utilized the user model (medical professional), making sure to hide sensitive patient data from anyone not authorized to use the system. In lew of registering, the assumption for this application is that the system administrator of the hospital has added authorized personal into the system.

### Contained in each file

views.py - The controller logic for rendering the different pages of the progam to the user in the view.

helpers.py - Helper functions dedicated to parsing the Json return objects used with the Gemini integration.

script.js - Using JS to get cookies/CSRF tokens, show notifications and impleement some Jquery to UI design (specifically adding and removing tests from the AI-diagnosis section).

styles.css - While bootstrap takes care of most of the look, this file focuses mainly on mobile responsiveness.

### Distinctiveness

This project is distintive in that it serves as a tool to aid ER medical staff in making decisions based on their patients. This project utilizes bootstrap and the fontawesome libraries to help make the site more user-friendly and mobile responsive, a departure of the mostly css projects throughout the course. The distinctive feature implementd in this project is the Gemini API, which uses their AI to assist the medical user in making and/or prioritizing tests of the patients in the system. 


### Complexity

Originally, there was a semi-reliable Medical diagnosis API that would work for Express applications, but was outdated and not maintained for python; after weeks and weeks of trying to find a workaround, and getting into contact with the authors of the API/repo, the decision was made to go entirely off of the AI API offered by Gemini. 

Finding a way to consistenly query and parse data brought back through the Gemini API was the first hurdle of this new route and required specialized helper functions that had to be written in JS and called in the script file. Second, I had to store and call and/or re-store patient information in local storage to cut down constantly calling the API whenever the page was loaded/reloaded. Not only was not doing this token-heavy, but also slowed down the application too much for a nice user experience. Now only the first call of each new symptom adjustment takes a bit longer, which each revisit to the diagnosis page is much more faster.

Lastly, the schemas for the database (in this case patients, medical tests, hospital visits, etc.) provided their own challenge in understanding the levels of normalization required to consistenly store and retrieve data, requiring the reworking of my databasee a few times.

### Requirements and startup

Please ensure that you have the following libraries installed:

django-boostrap-v5
fontawesome
google-generativeai

The application can be run normally by calling python manage.py runserver.



### Tech Stack

Django, Javascript, HTML, CSS, 

